# 模拟文件目录树
filesystem = {
    "A": {
        "D": {
            "index.js": "my JS code",
        },
        "E": {
            "text.py": "text python"        
        },
        "F": {
            "L":{},
            "M":{
                "circle.mp4": "a circle movie"
            },
            "N":{
                "square.mp3": "a square music,"
            }
        }
    },
    "B": {
        "X":{
            "draw.png": "picture of my drawing"
        },
        "Y":{
            "happy.c": "C source",
            "Q":{},
            "N":{}   
        }
    },
    "C": {
        "x.txt": "X-matrix",
    }
}


def resolve(fs, path):
    if not path:
        return directory
    name = path[0]
    print(f"当前查找：{name}")
    if name not in directory:
        raise FileNotFoundError(name)
    return resolve(fs[name], path[1:])


# 解析绝对路径
path = "/B/X/draw.png"
parts = path.strip("/").split("/")

result = resolve(filesystem, parts)

print("文件内容：", result)

