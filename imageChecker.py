
import os
from PIL import Image

# list = os.listdir(os.getcwd())
# print(list)

# removeList = []

count = 0
for dirname, dirnames, filenames in os.walk('.'):
    # print path to all subdirectories first.
    # for subdirname in dirnames:
    #     print(os.path.join(dirname, subdirname))

    # print path to all filenames.
    for filename in filenames:
        if filename.find("DS_Store") > 0 or filename.find(".py") > 0 or dirname.find(".idea") > 0:
            continue
        else:
            path = os.path.join(dirname, filename)
            # print(path)
            try:
                image = Image.open(path)
                # print(path)
                # color = image.getcolors()
                # print(image.getcolors())
                format = image.format

                image.load()
                image.close()
                # print(format)
                # print(format)
                if format == "JPEG" or format == "PNG":
                    pass
                else:
                    # print("remove")
                    # removeList.append(path)
                    print(path)
                    os.remove(path)
                    count += 1
            except:
                # print("except")
                # print("remove")
                # removeList.append(path)
                print(path)
                os.remove(path)
                count += 1
            finally:
                pass

print("Delete %d files" % count)
# print(len(removeList))
# for path in removeList:
#     os.remove(path)