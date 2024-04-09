import os
import re
import shutil
from difflib import SequenceMatcher

drive_paths = ["/mnt/server/OneTouch/Media/Anime",
                "/mnt/server/TwoTouch/Media/Anime",
               "/mnt/server/ThreeTouch/Media/Anime"]
user_tags = ["[Erai-raws] ", "[DKB] ", "[EMBER] ", "[killer neuron] "]
end_tags= ["[1080p][Multiple Subtitle]","[AMZN 1080p]", "[1080p][HEVC x265 10bit][Multi-Subs]"]
extra_tags = ["- Isekai Ittara Honki Dasu Part 2"]

def main():

    for drives in drive_paths:
        new_episodes_files = os.listdir('../')
        new_episodes_files.remove("pythonProject")
        shows = os.listdir(drives)
        #print(f"{new_episodes} \n{shows}")
        for episode_file in new_episodes_files:
            episode_no_user = episode_file
            for tag in extra_tags:
                episode_no_user = episode_no_user.replace(tag, "")


            episode_no_user = re.sub("- ([0-9]+)", "", episode_no_user)
            episode_no_user = re.sub("\[[a-z,A-Z,0-9, ,-]*\]", "", episode_no_user);
            episode_no_user = episode_no_user.replace(".mkv", "")

            episodes = episode_no_user.replace("[1080p][Multiple Subtitle]", "")

            most_similar = ""
            rating = 0.0
            for show in shows:
                if similar(episodes, show) > rating:
                    rating = similar(episodes, show)
                    most_similar = show
            if (rating > 0.5):
                print(f"{rating}: {episodes} -> {most_similar}")
                #check season

                child_files = os.listdir(f"{drives}/{most_similar}/")
                seasons = [x for x in child_files if
                    os.path.isdir(f"{drives}/{most_similar}/{x}")]
                season_folder = max(seasons, key=extract_number, default="")
                if season_folder == "metadata":
                    season_folder = ""
                if season_folder != "":
                    season_folder += "/"
                # print(season_folder)
                if os.path.exists(f"../{episode_file}"):
                    print(f"../{episode_file} -> {drives}/{most_similar}/{season_folder}{episode_file}")
                    shutil.move(f"../{episode_file}", f"{drives}/{most_similar}/{season_folder}{episode_file}")
                    print("Moved\n")
            print(f"{rating}: {episodes} -> {episode_no_user} -> {most_similar}")


def extract_number(f):
    s = re.findall("\d+$", f)
    return (int(s[0]) if s else -1, f)


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


if __name__ == '__main__':
    main()