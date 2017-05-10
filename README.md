# auto_qat_perf_test
QAT性能自动化测试工具，将openssl speed和cpa_sample_code命令集成到一起。
1. 先执行sh set_env.sh安装测试环境，主要是安装python-2.7.12和所需要的第三方包。
2. 然后执行python auto-qat_perf_test.py进行测试。测试结果存放在results文件夹中，里面包括在qat enable和disable之下的两次openssl speed测试结果，并且将两次测试结果使用柱状图表示在openssl.png文件中。
result_cpa_test.xlsx保存有处理之后的cpa_sample_code的结果，左边是策略，右边是对应的结果。
