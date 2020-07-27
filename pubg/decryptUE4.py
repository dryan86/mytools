import lief
from zlib import crc32
 
name = 'libtprt.so'
ue4_name = 'libUE4.so'
new_ue4_name = 'libUE4.so' + '.new'
 
with open(name, 'rb') as fp:
    tprt_bin = fp.read()
 
with open(ue4_name, 'rb') as fp:
    ue4_bin = fp.read()
 
ue4_binary = lief.parse(ue4_name)
ue4_section = ue4_binary.get_section('.text')
 
crc = crc32(tprt_bin) & 0xffffffff
key = (crc >> 16) & 0xff
 
ue4_text_data = []
# 
for i in range(ue4_section.size):
    tmpc = ue4_bin[ue4_section.offset + i]
    tmpce = tmpc ^ key
    ue4_text_data.append(tmpce)

tmp1 = ue4_bin[:ue4_section.offset]
tmp2 = ue4_bin[ue4_section.offset+ue4_section.size:]
new_ue4_bin = tmp1 + bytes(ue4_text_data) + tmp2
 
with open(new_ue4_name, 'wb') as fp:
    fp.write(new_ue4_bin)