#!/usr/bin/env python2.7
# -*- coding:utf-8 -*-
# author:yanshuo@inspur.com
import os
import sys
import subprocess
import shutil
import re
import matplotlib.pyplot as pyplot
import numpy
import xlsxwriter


def test_openssl(dir_result_sub):
    pattern_for_qat_status = re.compile(r"qat_dev(\d).*bsf: (\d*?\d+:\d*?\d+\.\d*?\d+).*state: (.*)")
    print "Begin to test openssl with QAT on"
    test_qat_on = subprocess.Popen(["/etc/init.d/qat_service", "start"])
    test_qat_on.wait()
    status_qat_on = subprocess.Popen(["/etc/init.d/qat_service", "status"], stdout=subprocess.PIPE)
    output_status_qat = status_qat_on.stdout.readlines()
    status_qat_on.wait()
    for item_qat_status in output_status_qat:
        qat_state_list = re.search(pattern_for_qat_status, item_qat_status)
        if qat_state_list is not None:
            qat_device_num = qat_state_list.groups()[0]
            qat_device_bus = qat_state_list.groups()[1]
            qat_device_state = qat_state_list.groups()[2]
            if qat_device_state.strip() == 'up':
                print "qat_dev%s bus_number:%s is %s successfully!" % (qat_device_num, qat_device_bus, qat_device_state)
            else:
                print "qat_dev%s bus_number:%s is %s! Please check!" % (qat_device_num, qat_device_bus, qat_device_state)
                sys.exit(1)
    # rsa
    result_openssl_rsa_qat_on = os.path.join(dir_result_sub, "result_openssl_rsa_qat_on.txt")
    file_openssl_rsa_qat_on = open(result_openssl_rsa_qat_on, mode='w')
    test_openssl_rsa_qat_on = subprocess.Popen(["/urs/local/ssl/bin/openssl", "speed", "-engine", "qat", "-elapsed", "-async_jobs", "72", "rsa"], stdout=file_openssl_rsa_qat_on)
    test_openssl_rsa_qat_on.wait()
    file_openssl_rsa_qat_on.close()

    filename_result_rsa_qat_off = os.path.join(dir_result_sub, "result_openssl_rsa_qat_off.txt")
    file_openssl_rsa_qat_off = open(filename_result_rsa_qat_off, mode='w')
    test_openssl_rsa_qat_off = subprocess.Popen(["/urs/local/ssl/bin/openssl", "speed", "-elapsed", "rsa"], stdout=file_openssl_rsa_qat_off)
    test_openssl_rsa_qat_off.wait()
    file_openssl_rsa_qat_off.close()
    # ecdh
    result_openssl_ecdh_qat_on = os.path.join(dir_result_sub, "result_openssl_ecdh_qat_on.txt")
    file_openssl_ecdh_qat_on = open(result_openssl_ecdh_qat_on, mode='w')
    test_openssl_ecdh_qat_on = subprocess.Popen(["/urs/local/ssl/bin/openssl", "speed", "-engine", "qat", "-elapsed", "-async_jobs", "36", "ecdh"], stdout=file_openssl_ecdh_qat_on)
    test_openssl_ecdh_qat_on.wait()
    file_openssl_ecdh_qat_on.close()

    filename_result_ecdh_qat_off = os.path.join(dir_result_sub, "result_openssl_ecdh_qat_off.txt")
    file_openssl_ecdh_qat_off = open(filename_result_ecdh_qat_off, mode='w')
    test_openssl_ecdh_qat_off = subprocess.Popen(["/urs/local/ssl/bin/openssl", "speed", "-elapsed", "ecdh"], stdout=file_openssl_ecdh_qat_off)
    test_openssl_ecdh_qat_off.wait()
    file_openssl_ecdh_qat_off.close()
    # ecdsa
    result_openssl_ecdsa_qat_on = os.path.join(dir_result_sub, "result_openssl_ecdsa_qat_on.txt")
    file_openssl_ecdsa_qat_on = open(result_openssl_ecdsa_qat_on, mode='w')
    test_openssl_ecdsa_qat_on = subprocess.Popen(["/urs/local/ssl/bin/openssl", "speed", "-engine", "qat", "-elapsed", "-async_jobs", "36", "ecdsa"], stdout=file_openssl_ecdsa_qat_on)
    test_openssl_ecdsa_qat_on.wait()
    file_openssl_ecdsa_qat_on.close()

    filename_result_ecdsa_qat_off = os.path.join(dir_result_sub, "result_openssl_ecdsa_qat_off.txt")
    file_openssl_ecdsa_qat_off = open(filename_result_ecdsa_qat_off, mode='w')
    test_openssl_ecdsa_qat_off = subprocess.Popen(["/urs/local/ssl/bin/openssl", "speed", "-elapsed", "ecdsa"], stdout=file_openssl_ecdsa_qat_off)
    test_openssl_ecdsa_qat_off.wait()
    file_openssl_ecdsa_qat_off.close()


def filter_openssl_rsa(filename_openssl_result, list_policy_filter_sub):
    data_display_temp = []
    data_display = []

    file_handler = open(filename_openssl_result, mode='r')
    data_file = file_handler.read()
    for index_policy, item_policy in enumerate(list_policy_filter_sub):
        pattern_data = re.compile(r"%s\s*(\d+.\d+).*?(\d+.\d+).*?(\d+.\d+).*?(\d+.\d+).*?(\d+.\d+)" % item_policy)
        result_filter = re.search(pattern=pattern_data, string=data_file).groups()
        for item_data_display in result_filter:
            data_display_temp.append(item_data_display)
    for item_data in data_display_temp:
        data_display.append(float(item_data))
    file_handler.close()
    return data_display

def filter_openssl_ecdh(filename_openssl_result, list_policy_filter_sub):
    data_display_temp = []
    data_display = []

    file_handler = open(filename_openssl_result, mode='r')
    data_file = file_handler.read()
    for index_policy, item_policy in enumerate(list_policy_filter_sub):
        pattern_data = re.compile(r"%s\s*(\d+.\d+).*?(\d+.\d+).*?(\d+.\d+).*?(\d+.\d+).*?(\d+.\d+)" % item_policy)
        result_filter = re.search(pattern=pattern_data, string=data_file).groups()
        for item_data_display in result_filter:
            data_display_temp.append(item_data_display)
    for item_data in data_display_temp:
        data_display.append(float(item_data))
    file_handler.close()
    return data_display


def plot_openssl_rsa(list_policy_first_sub, dir_result_sub):
    policy_block_data_list = []
    for item_policy_first in list_policy_first_sub:
        data_item = item_policy_first + " " + item_block
        policy_block_data_list.append(data_item)
    openssl_qat_on = filter_openssl_rsa(os.path.join(dir_result_sub, "result_openssl_ras_qat_on.txt"), list_policy_openssl_rsa)
    openssl_qat_off = filter_openssl_rsa(os.path.join(dir_result_sub, "result_openssl_rsa_qat_off.txt"), list_policy_openssl_rsa)
    figure_openssl = pyplot.figure("openssl_rsa")
    sub_figure = figure_openssl.add_subplot()
    bar_width = 0.5
    n_groups = len(policy_block_data_list)
    index = numpy.arange(n_groups)
    pyplot.bar(left=index, height=openssl_qat_on, width=bar_width, color='r', label='with_qat')
    pyplot.bar(left=index + bar_width, height=openssl_qat_off, width=bar_width, color='b', label='without_qat')
    pyplot.xlabel('Policy')
    pyplot.ylabel('Value')
    pyplot.xticks(index + bar_width, policy_block_data_list)
    pyplot.legend()
    pyplot.tight_layout()
    figure_filename = os.path.join(dir_result_sub, "openssl_rsa.png")
    pyplot.savefig(figure_filename)


def qat_cpa_test(dir_result_sub):
    test_qat_on = subprocess.Popen(["/etc/init.d/qat_service", "start"])
    test_qat_on.wait()
    path_file_result = os.path.join(dir_result_sub, "qat_cpa_result.txt")
    filename_result_cpa = open(path_file_result, mode='w')
    process_qat_cpa = subprocess.Popen(["cpa_sample_code", "runTests=63"], stdout=filename_result_cpa)
    process_qat_cpa.wait()
    filename_result_cpa.close()
    filename_result_cpa = open(path_file_result, mode='r')
    data_cpa_result = filename_result_cpa.read()
    list_data_spec_cfg1 = [13000, 45000, 80000, 133000, 144000, 152000, 7000, 12000, 43000, 53000, 69000, 70000, 9000, 32000, 62000, 101000, 128000, 134000, 102000, 44000, 135400, 141600, 95000, 43000, 129800, 135400]
    list_data_spec_cfg2 = [10000, 37000, 64000, 96000, 102000, 105000, 5000, 8000, 38000, 49000, 64000, 70000, 7000, 26000, 53000, 83000, 91000, 10300, 102000, 44000, 108100, 108900, 75000, 43000, 108900, 108900]

    data_list_display_policy_temp = []
    data_display = []
    list_block_cipher_aes128_cbc = ["64", "256", "512", "1024", "2048", "4096"]
    list_block_kasumi_f8 = ["40", "64", "256", "320", "512", "1024"]
    list_block_aes128_cbc_hmac_sha1 = ["64", "256", "512", "1024", "2048", "4096"]
    for item in list_block_cipher_aes128_cbc:
        temp_data = "AES128-CBC" + "-" + item
        pattern = re.compile(r"Cipher\sEncrypt\sAES128-CBC\s*API\s*?Data_Plane\sPacket\sSize\s*?%s\s.*\s*s.*\s.*\s.*\s.*\s.*\sThroughput.*?(\d+)" % item)
        result = re.search(pattern=pattern, string=data_cpa_result).groups()
        data_display.append(result[0])
        data_list_display_policy_temp.append(temp_data)
    for item in list_block_kasumi_f8:
        temp_data = "KASUMI_F8" + "-" + item
        pattern = re.compile(r"Cipher\sEncrypt\sKASUMI_F8\s*API\s*?Data_Plane\sPacket\sSize\s*?%s\s.*\s*s.*\s.*\s.*\s.*\s.*\sThroughput.*?(\d+)" % item)
        result = re.search(pattern=pattern, string=data_cpa_result).groups()
        data_display.append(result[0])
        data_list_display_policy_temp.append(temp_data)
    for item in list_block_aes128_cbc_hmac_sha1:
        temp_data = "AES128_CBC_HMAC_SHA1" + "-" + item
        pattern = re.compile(r"Algorithm\s*Chaining\s*-\s*AES128-CBC\s*HMAC-SHA1\s*API\s*?Data_Plane\sPacket\sSize\s*?%s\s.*\s*s.*\s.*\s.*\s.*\s.*\sThroughput.*?(\d+)" % item)
        result = re.search(pattern=pattern, string=data_cpa_result).groups()
        data_display.append(result[0])
        data_list_display_policy_temp.append(temp_data)
    list_huffman_policy = ["STATIC", "DYNAMIC"]
    list_huffman_direction = ["COMPRESS", "DECOMPRESS"]
    list_huffman_level = ["1", "2"]
    list_huffman_display = []
    list_data_huffman_display = []
    for item_huffman_policy in list_huffman_policy:
        for item_huffman_direction in list_huffman_direction:
            for item_huffman_level in list_huffman_level:
                policy_huffman_display = "Huffman" + "-" + item_huffman_policy + "-" + item_huffman_direction + "-level" + item_huffman_level
                pattern_huffman = re.compile(r"API\s*Data_Plane\s.*\s.*\sHuffman\s*Type\s*%s\s.*\sDirection\s*?%s\s.*\sCompression\s*Level\s*%s\s.*\s.*\s.*\s.*\s.*\s.*\s.*\s.*\sThroughput.*?(\d+)" % (
                    item_huffman_policy, item_huffman_direction, item_huffman_level))
                result_huffman = re.search(pattern_huffman, data_cpa_result).groups()
                list_huffman_display.append(policy_huffman_display)
                list_data_huffman_display.append(result_huffman[0])
    list_policy_display = data_list_display_policy_temp + list_huffman_display
    list_data_display = data_display + list_data_huffman_display
    list_data_diff = []
    list_data_spec_display = []
    if sys.argv[1] == "cfg1":
        list_data_spec_display = list_data_spec_cfg1
        for index_data_cfg1, item_data_cfg1 in enumerate(list_data_display):
            diff_data = float(item_data_cfg1) - 0.9 * float(list_data_spec_display[index_data_cfg1])
            list_data_diff.append(str(diff_data))
    elif sys.argv[1] == "cfg2":
        list_data_spec_display = list_data_spec_cfg2
        for index_data_cfg2, item_data_cfg2 in enumerate(list_data_display):
            diff_data = float(item_data_cfg2) - 0.9 * float(list_data_spec_display[index_data_cfg2])
            list_data_diff.append(str(diff_data))
    filename_cpa_result = os.path.join(dir_result_sub, "result_cpa_test.xlsx")
    workbook = xlsxwriter.Workbook(filename=filename_cpa_result)
    sheetone = workbook.add_worksheet("cpa_result")
    sheetone.set_column("A:A", 38)
    sheetone.set_column("B:D", 11)
    sheetone.write(0, 0, "Policy")
    sheetone.write(0, 1, "Value_Test")
    sheetone.write(0, 2, "Value_Spec")
    sheetone.write(0, 3, "Value_diff")
    sheetone.write(0, 4, "Results")
#    for index_write, item_write in enumerate(data_list_display_policy_temp):
#        sheetone.write(index_write + 1, 0, item_write)
#        sheetone.write(index_write + 1, 1, data_display[index_write])
#    length = len(data_list_display_policy_temp) + 1
#    for index_write_huffman, item_write_huffman in enumerate(list_huffman_display):
#        sheetone.write(length + index_write_huffman, 0, item_write_huffman)
#        sheetone.write(length + index_write_huffman, 1, list_data_huffman_display[index_write_huffman])
    list_ok_or_not = []
    for index_write_policy, item_write_policy in enumerate(list_policy_display):
        if float(list_data_diff[index_write_policy]) < 0.0:
            list_ok_or_not.append("FAIL")
        else:
            list_ok_or_not.append("PASS")
    for index_write_policy, item_write_policy in enumerate(list_policy_display):
        sheetone.write(index_write_policy + 1, 0, item_write_policy)
        sheetone.write(index_write_policy + 1, 1, list_data_display[index_write_policy])
        sheetone.write(index_write_policy + 1, 2, list_data_spec_display[index_write_policy])
        sheetone.write(index_write_policy + 1, 3, list_data_diff[index_write_policy])
        sheetone.write(index_write_policy + 1, 4, list_ok_or_not[index_write_policy])
    workbook.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:python auto_qat_perf_test.py cfg1/2!")
        print("Like:python auto_qat_perf_test.py cfg1")
        sys.exit(1)
    if os.path.exists("results") and os.path.isdir("results"):
        shutil.rmtree("results")
    os.mkdir("results")
    dir_result = os.path.join(os.getcwd(), "results")
    test_openssl(dir_result)
    list_policy_openssl_rsa = ["512", "1024", "2048", "3072", "4086", "7680","15360"]
    list_policy_openssl_ecdh = ["secp160r1", "nistp192", "nistp224", "nistp256", "nistp384", "nistp521", "nistk163", "nistk233", "nistk283", "nistk409",
                          "nistk571", "nistb163", "nistb233", "nistb283", "nistb409", "nistb571", "aX25519"]
    list_policy_openssl_ecdsa = ["secp160r1", "nistp192", "nistp224", "nistp256", "nistp384", "nistp521", "nistk163", "nistk233", "nistk283", "nistk409",
                          "nistk571", "nistb163", "nistb233", "nistb283", "nistb409", "nistb571", "aX25519"]

    plot_openssl_rsa(list_policy_openssl_rsa, dir_result)
    qat_cpa_test(dir_result)
