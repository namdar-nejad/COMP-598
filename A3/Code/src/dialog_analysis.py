import pandas as pd
import json, sys

file_path = sys.argv[3]
data = pd.read_csv(file_path)
df = data[['pony']]

speech_acts = [(each_string[0]).lower() for each_string in df.to_numpy()]

count_sparkle = speech_acts.count('twilight sparkle')
count_apple = speech_acts.count('applejack')
count_rarity = speech_acts.count('rarity')
count_pie = speech_acts.count('pinkie pie')
count_rainbow = speech_acts.count('rainbow dash')
count_shy = speech_acts.count('fluttershy')
total = len(speech_acts)

final_dict = {
        "count":
        {
            "twilight sparkle": count_sparkle,
            "applejack": count_apple,
            "rarity": count_rarity,
            "pinkie pie": count_pie,
            "rainbow dash": count_rainbow,
            "fluttershy": count_shy
        },

        "verbosity":
        {
            "twilight sparkle": round((count_sparkle/total),2),
            "applejack": round((count_apple/total), 2),
            "rarity": round((count_rarity/total), 2),
            "pinkie pie": round((count_pie/total), 2),
            "rainbow dash": round((count_rainbow/total), 2),
            "fluttershy": round((count_shy/total), 2)
        }
    }

json_path = sys.argv[2]
with open(json_path, "w") as outfile: 
    json.dump(final_dict, outfile, indent=4)
