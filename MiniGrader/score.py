import os

if __name__ == "__main__":
    files = list(filter(lambda x: os.path.isdir("submission/" + x), os.listdir("submission")))
    scores = open("scores.txt", "w+")
    #names = open("names.txt").read().splitlines()
    #names = list(map(lambda x: x.split("@")[0].lower(), names))
    names = []
    lists = [] #["0\n"] * len(names)
    missing = []
    for file in files:
        student = file.split('_')[-1].split('-')[0]
        if os.path.exists("submission/" + file + "/scores.txt"):
            score = int(open("submission/" + file + "/scores.txt").readlines()[-1].split(' ')[-1])
        else:
            score = 0
        scores.write(student + "," + str(score) + "\n")
        try:
            lists[names.index(student.lower())] = str(score) + "\n"
        except ValueError:
            missing.append(student + "," + str(score) + "\n")
    scores.close()
    output = open("canvas.txt", "w+")
    output.writelines(lists)
    output.writelines(missing)
