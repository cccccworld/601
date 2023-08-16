import cv2
import os
import xml.etree.ElementTree as ET

# 读取文本文件
with open(':/Users/86132/Desktop/yolo/yolo/txt/72.txt', 'r') as f:
    lines = f.readlines()

# 读取图片
img = cv2.imread('C:/Users/86132/Desktop/yolo/yolo/images/72.jpg')

# 处理文本文件，生成XML文件
for line in lines:
    items = line.strip().split()
    if len(items) == 5:
        x1, y1, x2, y2, class_name = float(items[0]), float(items[1]), float(items[2]), float(items[3]), items[4]
        rect = fr'<rect><x>{x1}</x><y>{y1}</y><width>{x2-x1}</width><height>{y2-y1}</height><object>{class_name}</object></rect>'
        xml_file = (
            fr'output_{os.path.basename(str(img)).replace("[", "").replace("]", "").replace(" ", "").replace("\t", "").replace("\n", "").split(".")[0]}.xml'
        )
        with open(xml_file, 'w') as f:
            f.write(rect)

# 检查XML文件中的矩形框是否相交
def is_intersect(rect1, rect2):
    x1, y1, x2, y2 = map(float, rect1.split('>')[1].split('<')[0].split('x')), map(float, rect1.split('>')[1].split('<')[2].split('y')), map(float, rect2.split('>')[1].split('<')[0].split('x')), map(float, rect2.split('>')[1].split('<')[2].split('y'))
    return not (x2 < x1 or x4 < x3 or y2 < y1 or y4 < y3)

def check_intersections(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    intersecting_boxes = []
    for box in root.iter('object'):
        xmin1, ymin1, xmax1, ymax1 = map(float, box.attrib['xmin'], box.attrib['ymin'], box.attrib['xmax'], box.attrib['ymax'])
        for box2 in root.iter('object'):
            if box == box2:
                continue
            xmin2, ymin2, xmax2, ymax2 = map(float, box2.attrib['xmin'], box2.attrib['ymin'], box2.attrib['xmax'], box2.attrib['ymax'])
            if is_intersect((xmin1, ymin1, xmax1, ymax1), (xmin2, ymin2, xmax2, ymax2)):
                intersecting_boxes.append((box, box2))
    return intersecting_boxes

# 检查XML文件中的矩形框是否相交，并输出结果到txt文件和图片中
def main():
    xml_file = 'outpu' \
            t.xml'  # 输出的XML文件名
    intersecting_boxes = check_intersections(xml_file)
    if intersecting_boxes:
        print("警告：以下矩形框相交：")
        for box1, box2 in intersecting_boxes:
            print("矩形框1：", box1)
            print("矩形框2：", box2)
        # 在图片上绘制相交矩形框，并保存图片到txt文件和图片中
        img = cv2.imread('input.jpg')
        for box in intersecting_boxes:
            cv2.rectangle(img, (int(box[0].attrib['xmin']), int(box[0].attrib['ymin'])), (int(box[0].attrib['xmax']), int(box[0].attrib['ymax'])), (0, 0, 255), 3)
            cv2.putText(img, box[0].attrib['class'], (int(box[0].attrib['xmin']), int(box[0].attrib['ymin']) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 3)
        cv2.imwrite('result.jpg', img)
        with open('result.txt', 'w') as f:
            f.write('矩形框相交情况：' + '相交' if intersecting_boxes else '不相交')
        print("结果已保存到：", os.path.abspath("result.jpg"))
        print("结果已保存到：", os.path.abspath("result.txt"))