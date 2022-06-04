import numpy as np
import matplotlib.pyplot as plt
from FuzzyInferenceSystem import *

# WILDAN FAJRI ALFARABI
# G64190060
# ga make library / package fuzzy bu saya, sekalian belajar :)
# ada beberapa range dari paper yang diubah agar output cog rainfall sesuai
# dengan yang di paper

def rules(temp, w_speed, humid):
    r = np.zeros(5)
    # 1 if (temp very_low) and (w_speed low) and (humid very_high) then rainfall very_low
    r_temp = np.min([temp.degree[4], w_speed.degree[3], humid.degree[0]])
    if r_temp >= r[4]:
        r[4] = r_temp

    # 2 if (temp medium) and (w_speed low) and (humid high) then rainfall medium
    r_temp = np.min([temp.degree[2], w_speed.degree[3], humid.degree[1]])
    if r_temp >= r[2]:
        r[2] = r_temp

    # 3 if (temp low) and (w_speed very_low) and (humid high) then rainfall medium
    r_temp = np.min([temp.degree[3], w_speed.degree[4], humid.degree[1]])
    if r_temp >= r[2]:
        r[2] = r_temp

    # 4 if (temp low) and (w_speed very_low) and (humid high) then rainfall low
    r_temp = np.min([temp.degree[3], w_speed.degree[4], humid.degree[1]])
    if r_temp >= r[3]:
        r[3] = r_temp

    # 5 if (temp low) and (w_speed very_low) and (humid low) then rainfall very_low
    r_temp = np.min([temp.degree[3], w_speed.degree[4], humid.degree[3]])
    if r_temp >= r[4]:
        r[4] = r_temp

    # 6 if (temp medium) and (w_speed high) and (humid low) then rainfall low
    r_temp = np.min([temp.degree[2], w_speed.degree[1], humid.degree[3]])
    if r_temp >= r[3]:
        r[3] = r_temp

    # 7 if (temp medium) and (w_speed very_high) and (humid low) then rainfall low
    r_temp = np.min([temp.degree[2], w_speed.degree[0], humid.degree[4]])
    if r_temp >= r[3]:
        r[3] = r_temp

    # 8 if (temp medium) and (w_speed very_high) and (humid medium) then rainfall very_high
    r_temp = np.min([temp.degree[2], w_speed.degree[0], humid.degree[2]])
    if r_temp >= r[0]:
        r[0] = r_temp

    # 9 if (temp very_high) and (w_speed very_high) and (humid medium) then rainfall high
    r_temp = np.min([temp.degree[0], w_speed.degree[0], humid.degree[2]])
    if r_temp >= r[1]:
        r[1] = r_temp

    # 10 if (temp very_high) and (w_speed very_high) and (humid high) then rainfall low
    r_temp = np.min([temp.degree[0], w_speed.degree[0], humid.degree[1]])
    if r_temp >= r[3]:
        r[3] = r_temp

    return r


def plotting(variables, rainfall, var_val):
    fig, ax = plt.subplots(2, 2, figsize=(10, 7))
    titles = ["temperatur", "humidity", "wind speed", "center of gravity rainfall"]
    ranges = [variables[0].range, variables[1].range, variables[2].range, variables[3].range]
    plots = []
    for i in range(4):
        range_v = ranges[i]
        i_s = int(i / 2)
        j_s = i % 2
        plots = []
        for k in range(len(ranges[0])):
            plot, = ax[i_s][j_s].plot(range_v[k], [0, 1, 0])
            plots.append(plot)
            ax[i_s][j_s].set_title(titles[i])
            if i == 3:
                vertical_lines = ax[i_s][j_s].axvline(x=rainfall.cog, color="black")
                legend_name = "center of gravity {}".format(rainfall.cog)
                ax[i_s][j_s].legend(handles=[vertical_lines],
                                    labels=[legend_name], loc='upper left', shadow=True)
            else:
                if variables[i].degree[k] != 0:
                    ax[i_s][j_s].annotate(text="degree {:.3f}".format(variables[i].degree[k]),
                                          xy=(var_val[i], variables[i].degree[k]))
                vertical_lines = ax[i_s][j_s].axvline(x=var_val[i], color="black")
                legend_name = "value {}".format(var_val[i])
                ax[i_s][j_s].legend(handles=[vertical_lines],
                                    labels=[legend_name], loc='upper left', shadow=True)
    fig.suptitle("Variabel")
    fig.legend(handles=plots, labels=["very-high", "high", "medium", "low", "very-low"],
               loc='lower center', shadow=True, ncol=len(ranges[0]))
    plt.show()


def fuzzyInferenceSystem(temp, humid, wind_s, rainfall, var_val):
    title = ["very-high :",
             "high      :",
             "medium    :",
             "low       :",
             "very-low  :"]

    category = ["very-high",
                "high",
                "medium",
                "low",
                "very-low"]
    variables = [temp, humid, wind_s, rainfall]
    print("------------------------------------------")
    print("---degree---")
    print("temperatur :", temp.triangular(var_val[0]))
    print("wind_speed :", wind_s.triangular(var_val[2]))
    print("humidity   :", humid.triangular(var_val[1]))

    rainfall.degree = rules(temp, wind_s, humid)
    print("")
    print("--rainfalls--")
    for i in range(len(rainfall.range)):
        print(title[i], rainfall.degree[i])

    rainfall.assign_axis()
    rainfall.centroidOfGravity()
    print("Center Of Gravity Value   :", rainfall.cog)
    print("Jadi, rainfallnya adalah  :", category[rainfall.curah_hujan()])
    plotting(variables=variables, rainfall=rainfall, var_val=var_val)


if __name__ == "__main__":
    temp_range = np.array([[25.53, 25.70, 25.90],
                           [25.34, 25.53, 25.73],
                           [25.14, 25.34, 25.53],
                           [24.94, 25.14, 25.34],
                           [24.74, 24.94, 25.14]], dtype=np.float32)

    wind_s_range = np.array([[1.73, 2.14, 2.55],
                             [1.13, 1.73, 2.14],
                             [0.91, 1.32, 1.73],
                             [0.5, 0.91, 1.32],
                             [0.09, 0.5, 0.91]], dtype=np.float32)

    humid_range = np.array([[80.99, 81.85, 82.72],
                            [80.13, 80.99, 81.85],
                            [79.26, 80.13, 80.99],
                            [78.41, 79.26, 80.13],
                            [77.55, 78.41, 79.27]], dtype=np.float32)

    rainfall_range = np.array([[6.25, 6.62, 6.99],
                               [5.88, 6.25, 6.62],
                               [5.51, 5.88, 6.25],
                               [5.14, 5.51, 5.88],
                               [4.77, 5.14, 5.51]], dtype=np.float32)

    temp = membershipVariable(temp_range)
    humid = membershipVariable(humid_range)
    wind_s = membershipVariable(wind_s_range)
    rainfall = membershipVariable(rainfall_range)

    # -------------------kasus di soal---------------------
    # tanya ke rainfall fuzzy sistem dengan urutan nilai [temperature, humidity, wind_speed]
    var_val = [25.2, 81, 0.964]
    fuzzyInferenceSystem(temp=temp, humid=humid, wind_s=wind_s, rainfall=rainfall, var_val=var_val)

    # -------------------tester1---------------------
    var_val = [25.39, 80, 2.47]
    fuzzyInferenceSystem(temp=temp, humid=humid, wind_s=wind_s, rainfall=rainfall, var_val=var_val)
