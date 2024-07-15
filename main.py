import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

data = pd.read_csv("umfrage.csv")

row_name = (" Welche Bedenken oder Vorbehalte hättest Du möglicherweise"
            " in Bezug auf die App?\n(Mehrfachauswahl möglich)")
missing_data_rows = data[data[row_name].isna()]
data = data.dropna(subset=[row_name])

def get_ages(data):
    ages = set()
    for datas in data["Alter"]:
        if isinstance(datas, float):
            continue
        else:
            ages.add(datas)

    liste = []
    for age in ages:
        liste.append(str(age))

    liste.sort()
    return liste

def get_age_distribution(data):
    liste = get_ages(data)
    palette = sns.color_palette('hls', len(liste))
    for i in range(len(liste)):
        plt.bar(liste[i], data["Alter"].value_counts().get(liste[i], 0), color=palette[i], alpha=.8)

    font = {"family": "arial", "size": 11}
    font_title = {"family": "arial", "size": 14}

    plt.ylabel("Anzahl der Mitglieder", labelpad=15, fontdict=font)
    plt.xlabel("Altersgruppe", labelpad=5, fontdict=font)
    plt.title("Alter der Mitglieder", pad=20, fontdict=font_title)
    plt.show()

def get_percentage_of_age_distribution(data):
    counts = []
    liste = get_ages(data)
    for x in liste:
        count = data["Alter"].value_counts().get(x,0)
        counts.append(count)
    explode = [0, 0, 0, 0, 0.1, 0, 0]
    plt.pie(counts, labels=liste, explode=explode, shadow=True, startangle=60, autopct='%1.1f%%',
            wedgeprops={'edgecolor':'black'})
    plt.title("Prozentualer Anteil der Alterklassen an Gesamtbefragten", pad=20, fontsize=14)
    plt.tight_layout()
    plt.show()

def get_age_distribution_and_app_interest(data):
    age_distribution_count = dict()

    liste = get_ages(data)
    for x in liste:
        plt.bar(str(x), data["Alter"].value_counts().get(x,0), color="blue")
        age_distribution_count[x] = data["Alter"].value_counts().get(x, 0)

    age_no_interest_dict = dict()
    age_interest_dict = dict()
    for age in liste:
        age_interest_dict[str(age)] = 0
        age_no_interest_dict[str(age)] = 0

    for index, row in data.iterrows():
        if row["Ich wäre an einer App interessiert."] == "Trifft zu":
            key = row["Alter"]
            age_interest_dict[key] += 1
        elif row["Ich wäre an einer App interessiert."] == "Trifft nicht zu":
            key = row["Alter"]
            age_no_interest_dict[str(key)] += 1
        else:
            continue

    interest_keys = list(age_interest_dict.keys())
    interest_values = list(age_interest_dict.values())
    no_interest_keys = list(age_no_interest_dict.keys())
    no_interest_values = list(age_no_interest_dict.values())

    percentages = []
    for key, value in age_distribution_count.items():
        try:
            percentage = (age_interest_dict[key] / age_distribution_count[key]) * 100
            percentages.append(int(percentage))
        except ZeroDivisionError:
            percentages.append(0)

    print(percentages)

    for i in range(len(interest_keys)):
        plt.plot(interest_keys[i],interest_values[i], "go", markersize=7)
        plt.text(interest_keys[i],interest_values[i],f'{percentages[i]}%', fontsize=14,
                 fontweight="bold", color="darkgreen")
        plt.plot(no_interest_keys[i], no_interest_values[i], "ro", markersize=7)

    plt.plot(interest_keys,interest_values,linestyle="-", linewidth=3, color="green",
             label="interessiert")
    plt.plot(no_interest_keys, no_interest_values, linestyle="-", linewidth=3, color="red",
             label="nicht interessiert")

    plt.title("Interesse an App pro Altersgruppe", pad=20, fontsize=14)
    plt.ylabel("Anzahl der Befragten", labelpad=15, fontsize=13)
    plt.xlabel("Altersgruppe", labelpad=5, fontsize=13)
    plt.grid(alpha=.4)
    plt.legend()
    plt.show()

def get_gender(data):
    female_df = data[data["Geschlecht"] == "Weiblich"]
    male_df = data[data["Geschlecht"] == "Männlich"]
    female_count = len(female_df)
    male_count = len(male_df)

    x = "Weiblich"
    y = "Männlich"

    palette = sns.color_palette('hls', 5)
    font = {"family": "arial", "size": 11}
    font_title = {"family": "arial", "size": 14}

    plt.bar(x, female_count,color=palette[0], alpha=.7, width=.2)
    plt.bar(y, male_count, color=palette[1], alpha=.7, width=.2)
    plt.xlabel("Geschlecht", labelpad=5, fontdict=font)
    plt.ylabel("Anzahl der Mitglieder", labelpad=15, fontdict=font)
    plt.title("Geschlecht der Mitglieder", pad=20, fontdict=font_title)

    plt.show()

def get_loyalty_rank(data):
    tiers = set()
    for datas in data["Auf welcher Stufe des Loyalitätsprogramm bist Du aktuell?"]:
        tiers.add(str(datas))

    rank_plant = data[data["Auf welcher Stufe des Loyalitätsprogramm bist Du aktuell?"] == "Plant (bis 499 Punkten)"]
    rank_grow = data[data["Auf welcher Stufe des Loyalitätsprogramm bist Du aktuell?"] == "Grow (500-999 Punkten)"]
    rank_bloom = data[data["Auf welcher Stufe des Loyalitätsprogramm bist Du aktuell?"] == "Bloom (ab 1.000 Punkten)"]
    plant_label = "Plant"
    grow_label = "Grow"
    bloom_label = "Bloom"

    palette = sns.color_palette('hls', 5)
    font = {"family": "arial", "size": 11}
    font_title = {"family": "arial", "size": 14}

    plt.bar(plant_label,len(rank_plant), alpha=.8, color=palette[1], width=.3)
    plt.bar(grow_label, len(rank_grow), alpha=.8, color=palette[2],width=.3)
    plt.bar(bloom_label, len(rank_bloom), alpha=.8, color=palette[3], width=.3)

    plt.xlabel("Loyalitätsstufe", labelpad=5, fontdict=font)
    plt.ylabel("Anzahl der Mitglieder", labelpad=15, fontdict=font)

    plt.title("Mitgliederstatus im Loyalitätsprogramm", pad=20, fontdict=font_title)

    plt.show()

def get_mobile_device(data):
    devices = set()
    for datas in data["Welches mobile Gerät verwendest Du am häufigsten, um Dr. Hauschka Produkte online zu kaufen?"]:
        devices.add(datas)

    tablet = data[data["Welches mobile Gerät verwendest Du am häufigsten,"
                        " um Dr. Hauschka Produkte online zu kaufen?"] == "Tablet"]
    smartphone = data[data["Welches mobile Gerät verwendest Du am häufigsten,"
                        " um Dr. Hauschka Produkte online zu kaufen?"] == "Smartphone"]
    laptop = data[data["Welches mobile Gerät verwendest Du am häufigsten,"
                            " um Dr. Hauschka Produkte online zu kaufen?"] == "Laptop/Computer"]
    tablet_label = "Tablet"
    smartphone_label = "Smartphone"
    laptop_label = "Laptop/Desktop"

    palette = sns.color_palette('hls', 10)
    font = {"family": "arial", "size": 11}
    font_title = {"family": "arial", "size": 14}

    plt.bar(tablet_label,len(tablet), color=palette[6], alpha=.7, width=.3)
    plt.bar(smartphone_label, len(smartphone), color=palette[7], alpha=.7, width=.3)
    plt.bar(laptop_label, len(laptop), color=palette[8], alpha=.7, width=.3)

    plt.xlabel("Gerät", labelpad=5, fontdict=font)
    plt.ylabel("Anzahl", labelpad=15, fontdict=font)

    plt.title("Gerätepräferenz beim Online-Kauf von Dr. Hauschka Produkten", pad=20, fontdict=font_title)

    plt.show()

def get_online_shopping_device_preference(data):
    options = set()
    for datas in data["Apps oder Browser für den Online-Einkauf - was ziehst Du generell vor?"]:
        options.add(datas)

    sorted_options = sorted(options)

    apps_and_browser = data[data["Apps oder Browser für den Online-Einkauf - "
                                  "was ziehst Du generell vor?"] == "Ich nutze sowohl  Apps"
                                                                      " als auch den Browser gleichermaßen gerne."]
    apps = data[data["Apps oder Browser für den Online-Einkauf - was ziehst Du generell vor?"] ==
                "Ich bevorzuge Apps."]
    apps_sometimes = data[data["Apps oder Browser für den Online-Einkauf - "
                                "was ziehst Du generell vor?"] ==
                          "Ich nutze Apps gelegentlich, bevorzuge  jedoch den Browser."]
    browser = data[data["Apps oder Browser für den Online-Einkauf "
                         "- was ziehst Du generell vor?"] == "Ich bevorzuge den Browser."]
    browser_sometimes = data[data["Apps oder Browser für den Online-Einkauf - "
                                   "was ziehst Du generell vor?"] ==
                             "Ich nutze den Browser gelegentlich, "
                                                                       "bevorzuge jedoch Apps."]
    no_exp = data[data["Apps oder Browser für den Online-Einkauf "
                         "- was ziehst Du generell vor?"] == "Ich habe noch keine Erfahrung "
                                                               "mit dem Einkauf über Apps."]
    no_preference = data[data["Apps oder Browser für den Online-Einkauf "
                         "- was ziehst Du generell vor?"] ==
                         "Ich habe keine klare Präferenz und wähle je nach Situation zwischen Apps und Browser."]

    counts = [len(apps), len(browser), len(no_preference), len(no_exp), len(apps_sometimes),
              len(browser_sometimes), len(apps_and_browser)]

    choice_values_series = pd.Series(data=counts, index=sorted_options)

    palette = sns.color_palette('hls', 10)
    font = {"family": "arial", "size": 11}
    font_title = {"family": "arial", "size": 14}

    ax = choice_values_series.plot(kind="bar", color=palette)

    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=palette[i]) for i in range(len(counts))]

    plt.legend(legend_handles, sorted_options, loc="upper right",
               bbox_to_anchor=(-0.1, 1), prop=font)
    plt.xticks([])
    plt.title("Präferenz beim Online-Einkauf: Apps oder Browser?", pad=20, fontdict=font_title)
    plt.subplots_adjust(left=0.5, right=0.9, top=0.9, bottom=0.1)
    plt.xlabel("Präferenz", fontdict=font, labelpad=10)
    plt.ylabel("Anzahl der Mitglieder", fontdict=font, labelpad=10)

    plt.show()

def get_percentage_of_app_usage_in_other_programs(data):
    total_user_idx = 12
    total_app_user_idx = 14
    total_user_df = data[data.iloc[:,total_user_idx] == "Ja"]
    total_user_count = len(total_user_df)
    total_app_user_df = data[data.iloc[:,total_app_user_idx] == "Ja"]
    total_app_user_count = len(total_app_user_df)

    total_not_using_app = total_user_count - total_app_user_count
    counts = [total_not_using_app, total_app_user_count]
    labels = ["Nutzen keine App", "Nutzen App"]
    colors = ['orange', 'blue']

    palette = sns.color_palette('hls', 2)
    font = {"family": "arial", "size": 11}
    font_title = {"family": "arial", "size": 14}

    plt.pie(counts, autopct='%1.1f%%', colors=palette[::-1],
                                wedgeprops={'edgecolor': (0.9, 0.9, 0.9), 'linewidth': 2, "alpha": .8},
                                textprops={"fontsize": 16, "color": (0.95, 0.95, 0.95), "fontstyle": "italic"})

    y_pos = .5
    for i, (label, color) in enumerate(zip(labels, palette[::-1])):
        plt.text(1.2, y_pos, '●', color=color, fontsize=15, alpha=0.8)
        plt.text(1.4, y_pos, label, fontdict=font)
        y_pos -= 1
        print(i, (label,color))
    plt.title("Der Anteil der Teilnehmer eines Treueprogramms,\n die eine App nutzen, in Prozent.",
              pad=10, fontdict=font_title)
    plt.tight_layout()

    plt.show()

def get_interest_usage_importance_in_app(data):
    answer_types = set()
    for datas in data["Ich wäre an einer App interessiert."]:
        answer_types.add(datas)

    positive_label = "Trifft zu"
    mostly_positive_label = "Trifft eher zu"
    neutral_label = "Teils-Teils"
    mostly_negative_label = "Trifft eher nicht zu"
    negative_label = "Trifft nicht zu"

    labels_list = [positive_label, mostly_positive_label, neutral_label, mostly_negative_label, negative_label]

    positive_interest = data[data["Ich wäre an einer App interessiert."] == labels_list[0]]
    mostly_positive_interest = data[data["Ich wäre an einer App interessiert."] == labels_list[1]]
    neutral_interest = data[data["Ich wäre an einer App interessiert."] == labels_list[2]]
    mostly_negative_interest = data[data["Ich wäre an einer App interessiert."] == labels_list[3]]
    negative_interest = data[data["Ich wäre an einer App interessiert."] == labels_list[4]]

    positive_usage = data[data["Ich wäre tatsächlich bereit,"
                                   " die App herunterzuladen und zu verwenden."] == labels_list[0]]
    mostly_positive_usage = data[data["Ich wäre tatsächlich bereit,"
                                          " die App herunterzuladen und zu verwenden."] == labels_list[1]]
    neutral_usage = data[data["Ich wäre tatsächlich bereit,"
                                  " die App herunterzuladen und zu verwenden."] == labels_list[2]]
    mostly_negative_usage = data[data["Ich wäre tatsächlich bereit,"
                                          " die App herunterzuladen und zu verwenden."] == labels_list[3]]
    negative_usage = data[data["Ich wäre tatsächlich bereit,"
                                   " die App herunterzuladen und zu verwenden."] == labels_list[4]]

    positive_importance = data[data[("Ich halte es für wichtig,"
                                     " dass das Programm eine App anbieten würde.")] == labels_list[0]]
    mostly_positive_importance = data[data[("Ich halte es für wichtig,"
                                            " dass das Programm eine App anbieten würde.")] == labels_list[1]]
    neutral_importance = data[data[("Ich halte es für wichtig,"
                                    " dass das Programm eine App anbieten würde.")] == labels_list[2]]
    mostly_negative_importance = data[data[("Ich halte es für wichtig,"
                                            " dass das Programm eine App anbieten würde.")] == labels_list[3]]
    negative_importance = data[data[("Ich halte es für wichtig,"
                                     " dass das Programm eine App anbieten würde.")] == labels_list[4]]

    answers_usage = [positive_usage, mostly_positive_usage, neutral_usage, mostly_negative_usage, negative_usage]
    answers_interest = [positive_interest, mostly_positive_interest,
                        neutral_interest, mostly_negative_interest, negative_interest]
    answers_importance = [positive_importance, mostly_positive_importance, neutral_importance,
                          mostly_negative_importance, negative_importance]

    answer_interest_rates = [len(i) for i in answers_interest]
    answer_usage_rates = [len(i) for i in answers_usage]
    answer_importance_rates = [len(i) for i in answers_importance]

    bar_width = 0.15

    fig, ax = plt.subplots()
    plt.axvspan(-1,2,color="green", alpha=0.15)
    plt.axvspan(2, 5, color="red", alpha=0.15)
    x = np.arange(len(labels_list))

    palette = sns.color_palette('hls', 10)

    plt.plot(labels_list, answer_interest_rates, color=palette[6],
    label="hätte Interesse an einer App", alpha=.8)
    plt.plot(labels_list, answer_interest_rates, "o", color=palette[6])
    plt.plot(labels_list, answer_usage_rates, color=palette[7],
    label="würde eine App herunterladen und nutzen", alpha=.8)
    plt.plot(labels_list, answer_usage_rates, "o", color=palette[7])
    plt.plot(labels_list, answer_importance_rates, color=palette[8],
    label="findet es wichtig eine App zu haben", alpha=.8)
    plt.plot(labels_list, answer_importance_rates, "o", color=palette[8])

    font = {"family": "arial", "size": 11}
    font_title = {"family": "arial", "size": 14}
    ticks = [0, 1, 2, 3, 4]
    plt.xticks(ticks, labels_list)
    plt.ylim(0, 300)
    plt.xlim(x[0]-1.5*bar_width, 4+1.5*bar_width)
    plt.ylabel("Anzahl der Antworten", labelpad=10, fontdict=font)
    plt.legend(prop=font)
    plt.title("Meinung der Befragten zu der potentiellen App", fontdict=font_title, pad=15)

    plt.show()

def get_what_appeal(data):

    choices_series = data.iloc[:, 16].str.split(';').explode()
    choice_counts = choices_series.value_counts()
    choice_counts_filtered = choice_counts[1:9]

    choice_counts_new = choice_counts_filtered.append(pd.Series([84], index=["Sonstiges"]))
    palette = sns.color_palette('hls', len(choice_counts_new))

    percentages = []
    for choice in choice_counts_new:
        percentage = int((choice/753) * 100)
        percentage = str(percentage)+"%"
        percentages.append(percentage)

    ax = choice_counts_new.plot(kind="bar", color=palette)

    for index, value in enumerate(choice_counts_new):
        ax.text(index, value, percentages[index], ha='center', va='bottom')

    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=palette[i])
                      for i in range(len(choice_counts_new))]

    font = {"family": "arial", "size": 11}
    font_title = {"family": "arial", "size": 14}

    plt.legend(legend_handles, choice_counts_new.index, loc="upper right",
               bbox_to_anchor=(-0.1, 1), prop=font)
    plt.ylabel("Anzahl der Befragten",labelpad=15, fontdict=font)
    plt.xlabel("Anreize", labelpad=15, fontdict=font)
    plt.xticks([])
    plt.title("Anreize zur Nutzung einer potenziellen App", fontdict=font_title, pad=15)
    plt.subplots_adjust(left=0.5, right=0.9, top=0.9, bottom=0.1)

    plt.show()

def get_what_concerns(data):

    choices_series = data.iloc[:, 21].str.split(';').explode()
    choice_counts = choices_series.value_counts()

    choice_counts_filtered = choice_counts[1:8]

    choice_counts_new = choice_counts_filtered.append(pd.Series([40], index=["Sonstiges"]))

    palette = sns.color_palette('hls', len(choice_counts_new))

    percentages = []
    for choice in choice_counts_new:
        percentage = int((choice / 753) * 100)
        percentage = str(percentage) + "%"
        percentages.append(percentage)

    ax = choice_counts_new.plot(kind="bar", color=palette)
    for index, value in enumerate(choice_counts_new):
        ax.text(index, value, percentages[index], ha='center', va='bottom')
    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=palette[i])
                      for i in range(len(choice_counts_new))]

    font = {"family": "arial", "size": 11}
    font_title = {"family": "arial", "size": 14}

    plt.legend(legend_handles, choice_counts_new.index, loc="upper right", bbox_to_anchor=(-0.1, 1), prop=font)
    plt.ylabel("Anzahl der Befragten", labelpad=5, fontdict=font)
    plt.xlabel("Bedenken", labelpad=15, fontdict=font)
    plt.xticks([])
    plt.title("Bedenken gegenüber einer potenziellen App", fontdict=font_title, pad=15)
    plt.subplots_adjust(left=0.5, right=0.9, top=0.9, bottom=0.1)

    plt.show()

def get_what_functions(data):

    choices_series = data.iloc[:, 17].str.split(';').explode()
    choice_counts = choices_series.value_counts()

    choice_counts_filtered = choice_counts[1:10]
    choice_counts_sonstiges = choice_counts[10:]

    summe = 0
    for index, value in choice_counts_sonstiges.items():
        summe += value

    choice_counts_new = choice_counts_filtered.append(pd.Series([summe], index=["Sonstiges"]))

    palette = sns.color_palette('hls', len(choice_counts_new))

    percentages = []
    for choice in choice_counts_new:
        percentage = int((choice / 753) * 100)
        percentage = str(percentage) + "%"
        percentages.append(percentage)

    ax = choice_counts_new.plot(kind="bar", color=palette)
    for index, value in enumerate(choice_counts_new):
        ax.text(index, value, percentages[index], ha='center', va='bottom')
    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=palette[i])
                      for i in range(len(choice_counts_new))]

    font = {"family": "arial", "size": 11}

    font_title = {"family": "arial", "size": 14}

    plt.legend(legend_handles, choice_counts_new.index, loc="upper right", bbox_to_anchor=(-0.1, 1), prop=font)
    plt.ylabel("Anzahl der Befragten", labelpad=5, fontdict=font)
    plt.xlabel("Funktionen", labelpad=15, fontdict=font)
    plt.xticks([])
    plt.title("Wichtige Funktionen einer potenziellen App", fontdict=font_title, pad=15)
    plt.subplots_adjust(left=0.5, right=0.9, top=0.9, bottom=0.1)
    plt.show()

def program_execute():

    # alter
    get_age_distribution(data=data)
    # geschlecht
    get_gender(data=data)
    # stufe des loyalitätprogramms
    get_loyalty_rank(data=data)
    # welches mobile gerät verwendet wird für den einkauf von produkten
    get_mobile_device(data=data)
    # apps oder browser -> präferenzen
    get_online_shopping_device_preference(data=data)
    # welches angebot in einer app am wichtigsten scheint
    get_interest_usage_importance_in_app(data=data)
    # welche anreize
    get_what_appeal(data=data)
    # welche bedenken
    get_what_concerns(data=data)
    # welche funktionen
    get_what_functions(data=data)
    # der anteil der teilnehmer eines treueprogramms, die eine app nutzen, in prozent
    get_percentage_of_app_usage_in_other_programs(data=data)


if __name__ == "__main__":
    program_execute()


