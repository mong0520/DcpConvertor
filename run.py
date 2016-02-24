# force update the dcp file to make nikon d750 can use d810's camera dcp file by using dcpTool
# update <UniqueCameraModelRestriction>Nikon D810</UniqueCameraModelRestriction> to
#        <UniqueCameraModelRestriction>Nikon D750</UniqueCameraModelRestriction> to
# Author: mongcheng@gmail.com
import os
from subprocess import call
class DcpConvertor():

    def __init__(self, b, d, x, o, ori_camera, new_camera):
        self.binary = b
        self.dcp_path = dcp_path
        self.xml_path = x
        self.out_path = o
        self.ori_camera = ori_camera
        self.new_camera = new_camera

    def list_files(self, path, ext_name):
        list = []
        for f in os.listdir(path):
            if f.endswith(ext_name):
                list.append(os.path.abspath(os.path.join(path, f)))
        return list

    def decompile_dcp_files(self, dcp_file_list):
        for f in dcp_file_list:
            output_filename = f.replace(".dcp", ".xml").replace(self.dcp_path, self.xml_path)
            print "Decompiliing %s ..." % f
            call([self.binary, "-d", f, output_filename])
            self.replace_string_in_file(output_filename, self.ori_camera, self.new_camera)

    def replace_string_in_file(self, file, ori_string, new_string):
        file_out = file.replace(ori_string, new_string)
        with open(file_out, "wt") as fout:
            with open(file, "rt") as fin:
                for line in fin:
                    fout.write(line.replace(self.ori_camera, self.new_camera))
        os.unlink(file)

    def compile_xml_files(self, xml_list):
        for f in xml_list:
            print "Compiling %s ..." % f
            output_filename = f.replace(".xml", ".dcp").replace(self.xml_path, self.out_path)
            call([self.binary, "-c", f, output_filename])

if __name__ == '__main__':
    binary = "dcpTool.exe"
    dcp_path = "input"
    xml_path = "xml"
    out_path = "output"
    dcp_convertor = DcpConvertor(binary, dcp_path, xml_path, out_path, "D810", "D750")

    dcp_list = dcp_convertor.list_files(dcp_path, ".dcp")
    dcp_convertor.decompile_dcp_files(dcp_list)

    xml_list = dcp_convertor.list_files(xml_path, ".xml")
    dcp_convertor.compile_xml_files(xml_list)
