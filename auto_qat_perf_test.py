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
    filename_result_qat_on = os.path.join(dir_result_sub, "result_openssl_qat_on.txt")
    file_openssl_qaton = open(filename_result_qat_on, mode='w')
    test_qat_openssl_on = subprocess.Popen(["openssl", "speed"], stdout=file_openssl_qaton)
    test_qat_openssl_on.wait()
    file_openssl_qaton.close()
    print "Begin to test openssl with QAT off"
    test_qat_off = subprocess.Popen(["/etc/init.d/qat_service", "shutdown"])
    test_qat_off.wait()
    status_qat_off = subprocess.Popen(["/etc/init.d/qat_service", "status"], stdout=subprocess.PIPE)
    output_status_qat = status_qat_off.stdout.readlines()
    status_qat_off.wait()
    for item_qat_status in output_status_qat:
        try:
            result_qat_status_shudown = re.search(pattern_for_qat_status, item_qat_status)
            if result_qat_status_shudown is not None:
                print "QAT shutdown fail! Please check!"
                sys.exit(1)
        except TypeError:
            print "QAT shutdown succefully!"
    filename_result_qat_off = os.path.join(dir_result_sub, "result_openssl_qat_off.txt")
    file_openssl_qatoff = open(filename_result_qat_off, mode='w')
    test_qat_openssl_off = subprocess.Popen(["openssl", "speed"], stdout=file_openssl_qatoff)
    test_qat_openssl_off.wait()
    file_openssl_qatoff.close()


def filter_openssl(filename_openssl_result, list_policy_filter_sub):
    #    list_policy_second = ["rsa  512 bits", "rsa 1024 bits", "rsa 2048 bits", "rsa 4096 bits", "dsa  512 bits", "dsa 1024 bits", "dsa 2048 bits",
    #                          "256 bit ecdsa (nistp256)", "384 bit ecdsa (nistp384)", "521 bit ecdsa (nistp521)"]
    #    list_policy_seoncd_secong = ["sign", "verify", " sign/s", "verify/s"]
    #    list_policy_third = ["256 bit ecdh (nistp256)", "384 bit ecdh (nistp384)", "521 bit ecdh (nistp521)"]
    #    list_policy_third_second = ["op", "op/s"]
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


def plot_openssl(list_policy_first_sub, list_block_first_sub, dir_result_sub):
    policy_block_data_list = []
    for item_policy_first in list_policy_first_sub:
        for item_block in list_block_first_sub:
            data_item = item_policy_first + " " + item_block
            policy_block_data_list.append(data_item)
    openssl_qat_on = filter_openssl(os.path.join(dir_result_sub, "result_openssl_qat_on.txt"), list_policy_filter)
    openssl_qat_off = filter_openssl(os.path.join(dir_result_sub, "result_openssl_qat_off.txt"), list_policy_filter)
    figure_openssl = pyplot.figure("openssl")
    sub_figure = figure_openssl.add_subplot()
    bar_width = 0.5
    n_groups = len(policy_block_data_list)
    index = numpy.arange(n_groups)
    pyplot.bar(left=index, height=openssl_qat_on, width=bar_width, color='r', label='enable_qat')
    pyplot.bar(left=index + bar_width, height=openssl_qat_off, width=bar_width, color='b', label='disable_qat')
    pyplot.xlabel('Policy')
    pyplot.ylabel('Value')
    pyplot.xticks(index + bar_width, policy_block_data_list)
    pyplot.legend()
    pyplot.tight_layout()
    figure_filename = os.path.join(dir_result_sub, "openssl.png")
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
    data_list_display_policy = []
    data_display = []
    list_block_cipher_aes128_cbc = ["64", "256", "512", "1024", "2048", "4096"]
    list_block_kasumi_f8 = ["40", "64", "256", "320", "512", "1024"]
    list_block_aes128_cbc_hmac_sha1 = ["64", "256", "512", "1024", "2048", "4096"]
    for item in list_block_cipher_aes128_cbc:
        temp_data = "AES128-CBC" + "-" + item
        pattern = re.compile(r"Cipher\sEncrypt\sAES128-CBC\s*API\s*?Data_Plane\sPacket\sSize\s*?%s\s.*\s*s.*\s.*\s.*\s.*\s.*\sThroughput.*?(\d+)" % item)
        result = re.search(pattern=pattern, string=data_cpa_result).groups()
        data_display.append(result[0])
        data_list_display_policy.append(temp_data)
    for item in list_block_kasumi_f8:
        temp_data = "KASUMI_F8" + "-" + item
        pattern = re.compile(r"Cipher\sEncrypt\sKASUMI_F8\s*API\s*?Data_Plane\sPacket\sSize\s*?%s\s.*\s*s.*\s.*\s.*\s.*\s.*\sThroughput.*?(\d+)" % item)
        result = re.search(pattern=pattern, string=data_cpa_result).groups()
        data_display.append(result[0])
        data_list_display_policy.append(temp_data)
    for item in list_block_aes128_cbc_hmac_sha1:
        temp_data = "AES128_CBC_HMAC_SHA1" + "-" + item
        pattern = re.compile(r"Algorithm\s*Chaining\s*-\s*AES128-CBC\s*HMAC-SHA1\s*API\s*?Data_Plane\sPacket\sSize\s*?%s\s.*\s*s.*\s.*\s.*\s.*\s.*\sThroughput.*?(\d+)" % item)
        result = re.search(pattern=pattern, string=data_cpa_result).groups()
        data_display.append(result[0])
        data_list_display_policy.append(temp_data)
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
    filename_cpa_result = os.path.join(dir_result_sub, "result_cpa_test.xlsx")
    workbook = xlsxwriter.Workbook(filename=filename_cpa_result)
    sheetone = workbook.add_worksheet("cpa_result")
    sheetone.set_column("A:A", 38)
    sheetone.write(0, 0, "Policy")
    sheetone.write(0, 1, "Value")
    for index_write, item_write in enumerate(data_list_display_policy):
        sheetone.write(index_write + 2, 0, item_write)
        sheetone.write(index_write + 2, 1, data_display[index_write])
    length = len(data_list_display_policy) + 1
    for index_write_huffman, item_write_huffman in enumerate(list_huffman_display):
        sheetone.write(length + index_write_huffman, 0, item_write_huffman)
        sheetone.write(length + index_write_huffman, 1, list_data_huffman_display[index_write_huffman])
    workbook.close()


if __name__ == "__main__":
    if os.path.exists("results") and os.path.isdir("results"):
        shutil.rmtree("results")
    os.mkdir("results")
    dir_result = os.path.join(os.getcwd(), "results")
    test_openssl(dir_result)
    list_policy_first = ["md2", "mdc2", "md4", "md5", "hmac(md5)", "sha1", "rmd160", "rc4", "des cbc", "des ede3",
                         "idea cbc", "seed cbc", "rc2 cbc", "rc5-32/12 cbc", "blowfish cbc", "cast cbc", "aes-128 cbc",
                         "aes-192 cbc", "aes-256 cbc", "camellia-128 cbc", "camellia-192 cbc", "camellia-256 cbc",
                         "sha256", "sha512", "whirlpool", "aes-128 ige", "aes-192 ige", "aes-256 ige", "ghash"]
    list_policy_filter = ["md2", "mdc2", "md4", "md5", "hmac\(md5\)", "sha1", "rmd160", "rc4", "des cbc", "des ede3",
                          "idea cbc", "seed cbc", "rc2 cbc", "rc5-32\/12 cbc", "blowfish cbc", "cast cbc",
                          "aes-128 cbc", "aes-192 cbc", "aes-256 cbc", "camellia-128 cbc", "camellia-192 cbc", "camellia-256 cbc",
                          "sha256", "sha512", "whirlpool", "aes-128 ige", "aes-192 ige", "aes-256 ige", "ghash"]
    list_block_first = ["16bytes", "64bytes", "256bytes", "1024bytes", "8192bytes"]
    plot_openssl(list_policy_first, list_block_first, dir_result)
    qat_cpa_test(dir_result)
