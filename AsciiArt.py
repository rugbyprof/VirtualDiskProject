'''
ASCII Art
Creates an ascii art image from an arbitrary image or list of images
It also writes the files out using hex values so I can create fake 
disk data for my class to read (for a disk simulation project).
 
@author: Terry Griffin
'''
import os
import sys
import argparse
from PIL import Image
 
class JpgToAsciiArt():
    def __init__(self):
        
        self.Images = [];
        self.FileCount = 0;
        self.AsciiOutDir = './'
        self.PreferredExtension = '.ascii'
        self.WidthRatio = .10
        self.HeightRatio = .10
        
    #######################################################
    # LoadDirectory
    # Loads a directory of images into a local structure
    ####################################################### 
    def LoadDirectory(self,dir_name):
        for filename in os.listdir(dir_name):
            fname,ext = os.path.splitext(filename)
            self.Images.append([dir_name,fname,ext]);
            self.FileCount += 1
    
    #######################################################
    # LoadFile
    # Loads a single file into a local structure
    #######################################################
    def LoadFile(self,file_name,dir_name='./'):
        fname,ext = os.path.splitext(file_name)
        self.Images.append([dir_name,fname,ext]);
        self.FileCount += 1    
        

    #######################################################
    # GetAsciiChar
    # Returns an ascii character based on luminosity
    #######################################################
    def GetAsciiChar(self,lum):		
        if lum > 250:
            character = " " #almost white
        elif lum > 230: 
            character = "`"
        elif lum > 200: 
            character = ":"
        elif lum > 175:
             character = "*"
        elif lum > 150:
             character = "+"
        elif lum > 125:
             character = "#"
        elif lum > 50:
             character = "W"
        else:
            character = "@" #almost black
        return character
    
    #######################################################
    # Convert
    # Converts whatever is in the local list of files
    #######################################################    
    def Convert(self):
        
        for dir_name,fname,ext in self.Images:
            
            inpath = os.path.join(dir_name,fname+ext)
            outpath =  os.path.join(self.AsciiOutDir,fname+self.PreferredExtension)
            print inpath,"=>",outpath

            
            im = Image.open(inpath)
            im = im.convert("RGB");
            
            width,height = im.size
            
            width = int(round(width * self.WidthRatio))
            height = int(round(height * self.HeightRatio))
            
            im=im.resize((width , height),Image.ANTIALIAS)  # shrink image, otherwise a character for 
                                                            # a pixel creates HUGE output
            im=im.convert("L")                              # convert to monochrome (0-255)

             
            ascii = open(outpath,"w")
            
            for y in range(0,im.size[1]):
                for x in range(0,im.size[0]):
                    lum=im.getpixel((x,y))
                    #hx.write(toHex(GetAsciiChar(lum)))
                    ascii.write(self.GetAsciiChar(lum))
        
                ascii.write("\n")
                #hx.write(toHex("\n"))
                
            ascii.close()
            #print os.path.getsize("./images_hex/"+name+".hex")
            
    def SetOutputDirectory(self,output_dir):
        self.AsciiOutDir = output_dir

    def SetFileExtension(self,file_ext):
        self.PreferredExtension = file_ext


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert file(s) to ascii art.")
    parser.add_argument('-directory', '-d', help="Directory of images to convert")
    parser.add_argument('-filename', '-f', help="File to convert.")
    parser.add_argument('-outpath', '-o', help="Output directory.")
    parser.add_argument('-extension', '-e', help="Extension for converted files.")
    args = parser.parse_args()
    if not (args.directory or args.filename):
        parser.error('No action requested, add -directory or -filename')
    else:
        Ascii = JpgToAsciiArt();
    
    if args.outpath:
        Ascii.SetOutputDirectory(args.outpath)
    if args.extension:
        Ascii.SetFileExtension(args.extension)
    
    if args.directory:
        Ascii.LoadDirectory(args.directory);
    else:
        Ascii.LoadFile(args.filename);
        
    Ascii.Convert();
    
    