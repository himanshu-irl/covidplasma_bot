# -*- coding: utf-8 -*-
"""
Created on Wed May 12 19:12:55 2021

@author: hverm
"""

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import textwrap
from datetime import datetime as dtm

def txt_insert(draw
               ,txt
               ,width
               ,offset
               ,font
               ,img_width):
    for line in textwrap.wrap(txt, width=width):
        draw.text((img_width/2, offset), line, font = font, align ="center", fill = (37,30,96), anchor='mm')
        offset += font.getsize(line)[1]
    
    return offset

# creating resource image from text
def create_img(row
               ,offset
               ,width
               ,image_path
               ,output_path
               ,font_path):
    
    # converting input-text to dict
    inp_dict = {}
    for index in list(row.index):
        value = str(row[index])
        inp_dict[index] = value
    
    resource_txt = f"#{inp_dict['resource_type']} #{inp_dict['city']}"
    input_txt = [resource_txt.upper()]
    
    # configuring info text
    info_txt = [inp_dict['info_txt_1'],inp_dict['info_txt_2'],inp_dict['info_txt_3']]
    info_txt = [x for x in info_txt if len(x.replace(' ',''))>0]
    for info in info_txt:
        input_txt.extend(info.split('\n'))
    
    # configuring contact text
    contact_txt = [inp_dict['contact_1'],inp_dict['contact_2'],inp_dict['contact_3']]
    contact_txt = [x for x in contact_txt if len(x.replace(' ',''))>0]
    contact_txt = ', '.join(contact_txt)
    if len(contact_txt.replace(', ',''))>0:
        contact_txt = f'Contact: {contact_txt}'
    else:
        contact_txt = ''
    input_txt.append(contact_txt)
    
    input_txt = [x for x in input_txt if len(x.replace(' ',''))>0]
    
    # opening template image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    # loading font and selecting font-size
    # If a font is already installed in your system, you can 
    # just give its name
    font_body = ImageFont.truetype(font_path, 100)
    font_head = ImageFont.truetype(font_path, 120)
    
    W, H = img.size
    
    # configuring timestamp
    dtmz = inp_dict['Timestamp']
    dtmz = dtm.strptime(dtmz, '%d/%m/%Y %H:%M:%S')
    dtmz = dtmz.strftime('%d-%b %I:%M %p')
    dtmz = f'Verified at {dtmz}'
    w, h = draw.textsize(dtmz)
    draw.text((W/2,550), dtmz, font=font_head, align='center', fill=(37,30,96), anchor='mm')
    
    # formatting remaining body in image
    count=0
    for item in input_txt:
        if len(item.replace(' ','')) > 0:
            offset = txt_insert(draw, item, width, offset, font_body, img_width=W)
        if count==0 and len(input_txt)<=4:
            offset+=150
        elif count==0 and len(input_txt)>4:
            offset+=50
        if count+1 <= len(input_txt)-1:
            if 'contact' in input_txt[count+1].lower() and len(input_txt)>4:
                offset+=40
            elif 'contact' in input_txt[count+1].lower() and len(input_txt)<=4:
                offset+=40
        if offset>=1700 and count+1 == len(input_txt)-1:
            offset=1700
        count+=1
        
    img.save(output_path)
    #img.show()
    return 'image saved...'
