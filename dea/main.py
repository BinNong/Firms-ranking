from pyDEA.core.data_processing.parameters import Parameters
from pyDEA.core.utils.dea_utils import clean_up_pickled_files
from pyDEA.core.utils.run_routine import RunMethodTerminal

# 设置参数（为了快速验证，先不采用配置的方式）,直接赋值。
para = Parameters()
# update_parameter方法用于向Parameters对象中设置参数。参数是以字典的形式进行存储，key是参数名，value是参数值。
para.update_parameter("DATA_FILE", "./data/DEAtestData.xlsx") # 模型输入数据（excel表格，也可以是csv文件）
para.update_parameter('DEA_FORM', 'env') # 一般保持不变
para.update_parameter('ORIENTATION', 'input') # 一般保持不变
para.update_parameter('OUTPUT_CATEGORIES', 'O2;O1') # 设置输入表格中哪些列是公司的产出系数，比如这里设置'O2;O1'，因为输入表格中这两列是公司的产出指标
para.update_parameter('MULTIPLIER_MODEL_TOLERANCE', '0') # 一般保持不变
para.update_parameter('RETURN_TO_SCALE', 'VRS') # 暂时保持i不变
para.update_parameter('INPUT_CATEGORIES', 'I2;I3;I1;I4') # 设置输入表格中哪些列是公司的投入系数，比如这里设置'I2;I3;I1;I4'，因为输入表格中这两列是公司的产出指标

# 获取计算函数（方法）
run_method = RunMethodTerminal(params=para
                               , sheet_name_usr="Sheet4" #这个参数表示使用哪张表单
                               , output_format='xlsx' #设置输出格式，也可设置成csv，如果是csv结果保存在data/DEAtestData_result中
                               , output_dir="./data")

run_method.run(para)
clean_up_pickled_files() #清除临时文件
