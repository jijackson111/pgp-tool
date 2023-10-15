import subprocess
import tempfile
import string
import random
import re

class CLI():
    def banner():
        line_break = '-'*30
        print(line_break)
        print('          PGP Tool')
        print(line_break)

    def show_options():
        print('Options:')
        print("1. Encrypt Message")
        print("2. Decrypt Message")
        print('3. List Keys')
        print('4. Generate Key Pair')
        print('5. Delete Key')
        print('6. Import Public Key')
        print('7. View Public Key')
        print('8. View Private Key')
        print('9. Sign Key')
        print('10. Edit Key')

    def select_option():
        option = int(input('\nChoose option: '))
        return option
    
class Keys():
    def gen_key():
        key_uid = input("Enter name for key: ")
        key_email = input("Enter email for key or leave blank: ")
        key_comment = input("Enter comment for key or leave blank: ")
        uid_string = '{}'.format(key_uid)
        if key_comment != '':
            uid_string += " ({})".format(key_comment)
        if key_email != '':
            uid_string += " <{}>".format(key_email)
        print("\nGenerating for:", uid_string)
        gen_command = 'gpg --quick-generate-key "{}"'.format(uid_string)
        print(gen_command)
        gen_keys = subprocess.Popen(gen_command, shell=True)
        gen_keys.communicate()

    def del_key():
        Keys.list_keys()
        key = str(input('Enter name of key to delete: '))
        command1 = 'gpg --delete-secret-keys "{}"'.format(key)
        command2 = 'gpg --delete-keys "{}"'.format(key)
        subprocess.run(command1, shell=True)
        subprocess.run(command2, shell=True)
        print('\n')
        Keys.list_keys()

    def import_pubkey():
        rand_list = list(string.ascii_letters) + list(str(range(10)))
        rand_str = ''.join(random.choices(rand_list, k = 8))
        pubkey_fn = '/tmp/tmp{}.gpg'.format(rand_str)       
        nano_command = "nano {}".format(pubkey_fn)
        nano_key = subprocess.call(nano_command, shell=True)
        import_command = 'gpg --import {}'.format(pubkey_fn)
        import_key = subprocess.Popen(import_command, shell=True)
        import_key.communicate()

    def show_pubkey():
        pubkey = str(input("Enter name of public key to show: "))
        command = 'gpg --export -armor {}'.format(pubkey)
        subprocess.run(command, shell=True)

    def show_privkey():
        pubkey = str(input("Enter name of private key to show: "))
        command = 'gpg --export-secret-keys -armor {}'.format(pubkey)
        subprocess.run(command, shell=True)

    def sign_key():
        signee = str(input("Enter key to sign: "))
        signing = str(input("Enter key to sign {} with".format()))
        command = 'gpg --sign-key --local-user {} {}'.format(signing, signee)
        subprocess.run(command, shell=True)

    def edit_key():
        key = str(input("Enter key to edit: "))
        command = "gpg --edit-key {}".format(key)
        subprocess.run(command, shell=True)

class Message():  
    def encrypt():
        rcp = str(input("Enter recipient email: "))
        sign = str(input("Enter email to sign message with: "))
        print('\nEnter message: ')
        message = str(input())
        bytes_msg = message.encode('utf-8')
        fp = tempfile.NamedTemporaryFile()
        fp.write(bytes_msg)
        filename = fp.name
        output_file = '{}.gpg'.format(filename)
        encrypt_command = "gpg --encrypt --sign --local-user {} --output {} --armor -r {} {}".format(
            sign, output_file, rcp, filename)
        subprocess.run(encrypt_command, shell=True)
        f = open(output_file, "r")
        print('\n')
        print(f.read())

    def decrypt():
        rn = random.randint(1000000, 9999999)
        encrypted_fn = '/tmp/tmp{}.gpg'.format(rn)
        nano_command = "nano {}".format(encrypted_fn)
        pgp_message = subprocess.call(nano_command, shell=True)
        decrypted_fn = encrypted_fn.replace('gpg', 'txt')
        decrypt_command = "gpg -d -o {} {}".format(decrypted_fn, encrypted_fn)
        decrypt = subprocess.run(decrypt_command, shell=True)
        fp = open(decrypted_fn, "r")
        print(fp.read())
    
class List():
    def list():
        output_bytes = subprocess.check_output("gpg --list-signatures", shell=True)
        output_string = output_bytes.decode('utf-8')
        output_list = output_string.split('\n')
        uids = []
        pubs = []
        keys = []
        sig_lists = []

        ln = 0
        sub_list_pos = 0
        last_sub_pos = 0
        for line in output_list:
            uid = re.search("uid", line)
            pub = re.search("pub", line)
            sigs = re.search("sig", line)
            if uid != None:
                match = re.findall("]\s.+", line)
                uids.append(match[0][2:])
            elif pub != None:
                if line[0] != '/':
                    pubs.append(line[6:])
            elif sigs != None:
                signature = line[13:]
                diff = ln - last_sub_pos
                if diff == 1:
                    current_sublist = sig_lists[sub_list_pos]
                    current_sublist.append(signature)
                elif diff == 5:
                    sig_lists.append([signature])
                else:
                    sub_list_pos += 1
                last_sub_pos = ln
            else:
                match = re.search("([A-Z]+[0-9]+)+", line)
                if match != None:
                    keys.append(line[6:])
            ln += 1

        for i in range(len(uids)):
            print("User ID:", uids[i])
            print("Public Key:", keys[i])
            print("Key Info:", pubs[i])
            siglist = sig_lists[i]
            print("User Signature:", siglist[0])
            if len(siglist) > 1:
                for n in range(1, len(siglist)):
                    print("Other Signature:", siglist[n])
            print('\n')

