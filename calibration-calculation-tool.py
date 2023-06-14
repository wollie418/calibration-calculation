
def ParseJson(json_file_path):
  import json
  with open(json_file_path, 'r') as f:
    data = json.load(f)

  real_width = data['real_width']
  vertex1 = data['vertex1']
  vertex2 = data['vertex2']
  vertex3 = data['vertex3']
  vertex4 = data['vertex4']

  return real_width, vertex1, vertex2, vertex3, vertex4

def computeDistance(point1, point2):
  import math as m
  distance = (point1['x'] - point2['x'])**2 + (point1['y'] - point2['y'])**2
  distance = m.sqrt(distance)
  return distance

def computePrecision(real_length_mm, image_length_pixel):
  return real_length_mm / image_length_pixel


def main_process(json_file_path):
  # 1. 对输入数据进行匹配。使用JSON配置文件作为输入。 
  real_width, vertex1, vertex2, vertex3, vertex4 = ParseJson(json_file_path)

  # 2. 计算图像的像素宽度
  board_image_width = computeDistance(vertex1, vertex2)

  # 3. 计算宽度的成像精度(mm/pixel)
  image_precision = computePrecision(real_width, board_image_width)

  # 4. 使用成像精度计算实际高度
  board_real_height = computeDistance(vertex1, vertex4) * image_precision

  # 5. 计算两条对角线的实际长度
  diagonal_line1_length = computeDistance(vertex1, vertex3) * image_precision
  diagonal_line2_length = computeDistance(vertex2, vertex4) * image_precision

  return image_precision, diagonal_line1_length, diagonal_line2_length


if __name__ == '__main__':
  
  import sys
  if len(sys.argv) != 2:
    print("Usage: {} Json-file-path".format(sys.argv[0]))
    print("\texample: python calibration-calculation-tool.py sample.json")
    exit(-1)

  # 确定json文件是否存在
  import os
  if not os.path.exists(sys.argv[1]):
    print("Can not found the Json file at {}".format(sys.argv[1]))
    exit(-2)

  image_precision, diagonal_line1_length, diagonal_line2_length = main_process(sys.argv[1])

  print("Image Precision: {} pixel/mm".format(image_precision))
  print("Diagonal ①③: {} mm".format(diagonal_line1_length))
  print("Diagonal ②④: {} mm".format(diagonal_line2_length))



