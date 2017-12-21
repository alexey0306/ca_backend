# Import section
import datetime,hashlib,binascii,rncryptor,base64, math, os,json, shutil
from app.globals.saferoom import MIME_TYPES,MIME_DEFAULT
from asn1crypto import cms
from OpenSSL import crypto

# Getting the list of recipients from CMS structure
def get_recipients(content):
	
    try:

        # Getting the content betweeb prefix and suffix
        result = content.split("__")[-2]
        recipients = []
        
        # Analyzing the CMS structure
        ci = cms.ContentInfo.load(base64.b64decode(result))
        for rec in ci['content']['recipient_infos']:
            rid = rec.chosen['rid'].chosen
            recipients.append(hex(rid['serial_number'].native).replace("0x","").replace("L",""))
        return recipients
    except Exception as e:
        return []



# Function used to dump PFX into Public and Private key files
def dump_pfx(pfx_file,password):
    
    try:
        # Reading the PFX file
        pfx = crypto.load_pkcs12(file(pfx_file, 'rb').read(),password)
        
        # Dumping the private key into file
        private = "%s.private" % pfx_file
        with open(private,"wb") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM,pfx.get_privatekey()))
        
        # Dumping the certificate
        public = "%s.public" % pfx_file
        with open(public,"wb") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM,pfx.get_certificate()))
        
        return private,public        
        
    except Exception as e:
        raise Exception("Error while dumping the PFX file: %s" % str(e))
    


# Calculate the MD5 value for the specified string
def md5_string(source):
    m = hashlib.md5()
    m.update(source)
    return m.hexdigest()

# Calculate the file's MD5
def md5_file(filename):
    with open(filename,"rb") as f:
        data = f.read()
        md5 = hashlib.md5()
        md5.update(data)
        hash = md5.digest()
        return binascii.hexlify(hash)

def getMime(fileName):

    # Getting file extension
    array = fileName.split(".")
    extension = array[-1]
    try:
        return MIME_TYPES[extension]
    except KeyError:
        return MIME_DEFAULT

def encrypt_string(string,key):
    cryptor = rncryptor.RNCryptor()
    encrypted_string = cryptor.encrypt(string,key)
    return base64.b64encode(encrypted_string)

def decrypt_string(string,key):
    cryptor = rncryptor.RNCryptor()
    encrypted_string = base64.b64decode(string)
    decrypted_string = cryptor.decrypt(encrypted_string,key)
    return decrypted_string

def encrypt_note(noteContent,password):
    cryptor = rncryptor.RNCryptor()
    encrypted_data = cryptor.encrypt(noteContent,password)
    return base64.b64encode(encrypted_data)

def encrypt_data(data,password):
    cryptor = rncryptor.RNCryptor()
    encrypted_data = cryptor.encrypt(data,password)
    return encrypted_data

def decrypt_note(noteContent,password):
    cryptor = rncryptor.RNCryptor()
    content = base64.b64decode(noteContent)
    decrypted_data = cryptor.decrypt(content,password)
    return decrypted_data

def decrypt_data(data,password):
    cryptor = rncryptor.RNCryptor()
    decrypted_data = cryptor.decrypt(data,password)
    return decrypted_data
	
def get_icon(mime):
	
	if mime in ["application/pdf"]:
		
		return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABIAAAAYCAYAAAD3Va0xAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEwAACxMBAJqcGAAAAbpJREFUOI3d07FLG2EYx/Hv++aSO/UMzXnapXa4iulSREFcHDo4dOigIq51cirVTTdXEZHi3yBCl0AGMYM4CBHBQRfB1Qh1CBK9XJpr9O7tmlB7Mb2l9De+D+/nfd/nfV9xmkx+QohtIE2bvJqZCXsd56hndHRKzM8HzTUZCvH1OQiAFELqtv2+dnZWUGtrsqUm4cVzkObotj1VbTT2mjEZNSEqXbb9wfP9vFJKxIIAjIGBj97qak4pJTqCHjzvKWzaW1n5pnUClY+PSVkWmmm2jCshZsVpKqU6wf6UWD36zyChaWiW9ffQu8tLAN4eHjK4uflbveX6NdvGmptDdxy8kxMquRz2wgLG0BAJ06R7bAxjeJjv6+vRO9L6+uhfXKSSz/N6a4vukRFeLi1xt7+PSCZpXF8T1Ov4Fxftj9YolfCKRR5vbzGyWX6cn+MViwSuy2O5jPJ9fl5dtYd6xsd5s7tLWK/jHhzQOzmJs7PzZIOb0/KyjWyWwY0NSsvLPNzcEPo+iUwGqeuEtRpBtUoinSZw3WgokclgTkxwXyhErt52R3HyD36REO7jIgoqUir1JQ4Wwp1Q6vMvijqWZ56DUooAAAAASUVORK5CYII="
	
	elif mime in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document","application/msword","application/vnd.ms-word"]:
	
		return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEwAACxMBAJqcGAAAAh5JREFUSIntlU1PE2EUhZ9SButAoYXSKhDT2AYt1miaGEn8WJjgolvj2p3uce/Cv+Be/QEmxo1QQZJiYpCYiJWGRkskJm3SLwcpLaWdzrgYmOlM28QNURPO6s577tzz3nNv8toCs29UjhA9R1n8WODfEOht/XCJAiMDfQBsVxuUdus6J56wc3rIAcD3QhVFNZZv3O3AIdgByEh71BpKZ4HwxCDPH0QAWEoWuP90TefuXT/Dw2gQgLtPVvm09QsAe4+NV7PTuESBuqxw5VEcMARMFn3YlNityQBMB4cR7AYdvezT45mwV48jfhcuUQBgOVWisi+bLDIJNJoK8VRRtyTiHwLgrLef0JhTz7t90YvNpsW3pjz6+VwihxVtQ15cL+jxjfPaz9FLPlOO3yMS9A1oAhdGAZCbKkvJAla0CcRTRZqKNsCb50Y0gQN7topVUxd+j0jA2w/Au68lyjUZK9oEdvZkVtISAFPjTq4G3Eye0m77bPkHG9kyADPhUf32APOf2+0ByxYdYjGZ59rkMACP74QAUFSVWCKHWxQIjTkJTwxysk9bzaai8raDPR07AEzJAZ9mwUpaoliuM98yyEN73n/7yXa18ecCWanGRqZsOnu9phVO5yps5ismbq6LPV0FABZaumgqKrEvRpFYIm/iFtbzdEPHGQC8/JjV48LOPlLFsODFagb5YNNKZTNnhe34RfvrAr2gdN+x/wG/AfAaveWC8KuAAAAAAElFTkSuQmCC"
	
	elif mime in ["application/vnd.ms-excel","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
	
		return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEwAACxMBAJqcGAAAAhJJREFUSIntlV1Ik1EYx3/vh2tkNVg4i+G0QWoSKKgYmVd9QCUEQgTh5kV5UdSFFtVNNco+6aKLKIjQvibRx0VdWCALQpKIknajIbUoNtKVWS3enNvetwvjwHBzW7SLoP/d8z/neX4855yHI5n3NxrkUXI+i/8HZCU1lVmgqLjqNqHIM3zDMLjxoo9oPAZAmXUp6ysaxP5JLcJdvy97QCwRZ8mixRzesEN4toVWTvb3oMgyV7cfpaF0pVhr6T6QtoO0R3TGd42BwCsRH1zrprzIwd6mbUnFz/qu83BkMC1AmmsO7BYbzzt7sM63AOAPjVJZvIx5agEAT94O0Xy5g7ieyL0DgNC3MO23Toi42l4uio99n8Dt9cxZPCMAoG9kkAsDt5O8hK7TevMI4ciXTOnZPdP3kx+T4h/TGsGv4WxSMwPWOGs41bwnybOYF+B1HRPH9ccAu8VGr+s4qqwA8OZzEN3QAagtWTELnEqKutrhSbVgVk08aD/H8iIHAJGoxrqLu9Gmp2h0VgNQ76hi9NMHhscCuXUgSRLnW/ZRV1IlvF13ThOYCNHV381Q8LXwL209RIWtNDfAzlVbaKvfLOIrz+5zz/8YmJnyNq8HLTYFQKHJTK+7i0KTOSVg1qApskxr7UZMvy/QMAy8Lx/xMxZNSmxy1lBZXCbipwE/w+PvMgP+tv79/yD/H44O4/mG5FW/AEtwoL2+bvXpAAAAAElFTkSuQmCC"
	
	
	elif mime in ["application/vnd.ms-powerpoint","application/vnd.openxmlformats-officedocument.presentationml.presentation"]:
	
		return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEwAACxMBAJqcGAAAAPpJREFUSIljvBut9p+BhoCJloaPWjA4LGAhpICZX4SBkY0dRez/r58Mfz+9ZWD4TzgBErRALKuHgVPbEkP8z+snDG+XdTJ8Pb0Lr36Sguj/r+8M///+gbhMVIZBPG8iA4eqIfUseJTvyHA/QZfh7bJOiAAjEwOvfTD1LGBgYGBg+P+P4dvZvXAuM58wXuUE4wAZsMmqMfz//YuBzzUaLvb7+X3qWSBZtQiF///nd4ZP+1ZQz4K/H98w/P/3l+H/rx8MP+9fZfiwaQbD75ePqGfBkwofhr+f35OiZSQUFV9P72L49eQ2AwMDA8P/3z9JtoBxtEYb/hbQHAAAMg1SBMrMhTAAAAAASUVORK5CYII="
	
	else:
	
		return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEwAACxMBAJqcGAAAAPdJREFUSInt1rFKBDEQBuDvPPUQfJ+rhLWxsj57n8FWuMrOJ9HGSi0EsfIQC5/Bxv464U6LnBLi7iZ7arc/LCEz/84/kwlJBn5ijAMMa3wprjFrI2zUBL/CTkHwCnfYK+B+4xRnhdwpbvDWJpJWMMR7h4QeMcFFk0gqsA4ecITLOpHfClTCUu3jRWj6OCakO6VajfcFwecYRfNXbGMr/n+zNNUaPK++GNOU9Bc9aMW/C+SW6AS7Gc4c503OXAUfGT8s25y5ChozK0XfA/oe6HuQzJfCkbsuRljEhrSCW+HSp9vV+RX8GIexcVBD7PJsibEQHgFPsfETWgYrD24yukcAAAAASUVORK5CYII="
