import numpy as np

class membershipVariable:
    def __init__(self, ranges):
        self.range = ranges
        self.degree = np.zeros(5, dtype=np.float32)
        self.cog = 0
        self.x_axis = []
        self.y_axis = []

    def triangular(self, x):
        for i in range(len(self.range)):
            if x == self.range[i][1]:
                self.degree[i] = 1
            elif self.range[i][0] < x < self.range[i][1]:
                self.degree[i] = float((x - self.range[i][0])) / float((self.range[i][1] - self.range[i][0]))
            elif self.range[i][1] < x < self.range[i][2]:
                self.degree[i] = float((self.range[i][2] - x)) / float((self.range[i][2] - self.range[i][1]))
            else:
                self.degree[i] = 0
        return self.degree

    def centroidOfGravity(self):
        x = self.x_axis
        y = self.y_axis
        print(x, y)
        coa_x_area = []
        areas = []
        for i in range(len(x) - 1):
            if y[i] == 0 and y[i + 1] == 0:
                continue
            if y[i] == 0 or y[i + 1] == 0:
                # segitiga
                area = np.trapz([y[i], y[i + 1]], [x[i], x[i + 1]])
                center = ((x[i + 1] * 2) + x[i]) / 3
                cog = area * center
            elif y[i] == y[i + 1]:
                # persegi
                area = np.trapz([y[i], y[i + 1]], [x[i], x[i + 1]])
                center = (x[i] + x[i + 1]) / 2
                cog = area * center
            else:
                # trapesium
                if y[i] > y[i + 1]:
                    mid = y[i + 1]
                    upper = y[i]
                else:
                    mid = y[i]
                    upper = y[i]

                area_atas = np.trapz([mid, upper], [x[i], x[i + 1]])
                area_bawah = np.trapz([0, mid], [x[i], x[i + 1]])
                center_atas = ((x[i + 1] * 2) + x[i]) / 3
                center_bawah = (x[i] + x[i + 1]) / 2
                cog_atas = area_atas * center_atas
                cog_bawah = area_bawah * center_bawah
                cog = cog_atas + cog_bawah
                area = area_atas + area_bawah
            coa_x_area.append(cog)
            areas.append(area)
        self.cog = np.round(np.sum(np.sum(np.array(coa_x_area)) / np.sum(np.array(areas))), 2)

    def assign_axis(self):
        flag = 1
        idx_degree = 0
        self.x_axis = []
        self.y_axis = []

        while flag:
            if self.degree[idx_degree] != 0:
                a = self.range[idx_degree][0]
                b = self.range[idx_degree][1]
                c = self.range[idx_degree][2]
                y = self.degree[idx_degree]

                x_left = y * (b - a) + a
                x_right = c - (y * (c - b))

                self.y_axis.append(y)
                self.y_axis.append(y)
                self.x_axis.append(x_left)  # kiri
                self.x_axis.append(x_right)  # kanan
            else:
                self.y_axis.append(0)
                if idx_degree < len(self.degree) - 2:
                    if idx_degree > 0:
                        if self.degree[idx_degree + 1] != 0:
                            self.x_axis.append(self.range[idx_degree + 1][0])
                        elif self.degree[idx_degree - 1] != 0:
                            self.x_axis.append(self.range[idx_degree - 1][2])
                        else:
                            self.x_axis.append(0)
                    else:
                        if self.degree[idx_degree + 1] != 0:
                            self.x_axis.append(self.range[idx_degree + 1][0])
                        else:
                            self.x_axis.append(0)
                if idx_degree == len(self.degree) - 2:
                    if self.degree[idx_degree - 1] != 0:
                        self.x_axis.append(self.range[idx_degree - 1][2])
                    else:
                        self.x_axis.append(0)
            if idx_degree == len(self.degree) - 1:
                flag = 0
            else:
                idx_degree += 1

    def curah_hujan(self):
        idx = -1
        for i in range(len(self.range)):
            if self.range[i][0] <= self.cog < self.range[i][2]:
                idx = i
                break
        return idx