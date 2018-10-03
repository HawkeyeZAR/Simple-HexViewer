import binascii

class ToHex(object):
    '''
    Contains functions to convert binary data into hex data
    '''
    def convert_to_hex(self, file_name):
        '''
        Reads the file in binary mode.

        convert all binary data to hex.

        Return hex data
        '''
        index = 0
        hex_data = {}
        with open(file_name, "rb") as bf:
            while True:
                rf = bf.read(16)
                hex_txt = binascii.hexlify(rf)
                new_str = hex_txt.decode('ascii')
                if len(rf) == 0:
                    break
                h_val = '-'.join(new_str[i:i+2] for i in range(0, len(new_str), 2))
                # Convert index to hex
                hex_index = "{:08X}".format(index) + ': '
                hex_text = self.replace_invalid_char(rf)
                index += 16
                hex_data[hex_index] = [h_val.upper(), hex_text]
                #print(hex_line)
            return hex_data

    def replace_invalid_char(self, char_str):
        '''
        This function is needed to convert the hex data properly
        '''
        fixed_string = ''
        for char in char_str.decode('ascii', errors="replace"):
            if char in "\u2028\u2029\t\n\r\v\f\uFFFD":
                char = "."
                fixed_string += char
            elif not 0x20 <= ord(char) <= 0xFFFF: 
                char = "."
                fixed_string += char
            else:
                fixed_string += char
        return fixed_string
