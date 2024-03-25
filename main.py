import os
import re
import shutil
from difflib import SequenceMatcher

drive_paths = ["/mnt/server/OneTouch/Media/Anime",
                "/mnt/server/TwoTouch/Media/Anime",
               "/mnt/server/ThreeTouch/Media/Anime"]


def main():

    for drives in drive_paths:
        new_episodes_files = os.listdir('../')
        new_episodes_files.remove("pythonProject")
        new_episodes_no_user = [s.replace("[Erai-raws] ", "") for s in new_episodes_files]
        new_episodes = [s.replace("[1080p][Multiple Subtitle]", "") for s in new_episodes_no_user]
        shows = os.listdir(drives)
        #print(f"{new_episodes} \n{shows}")
        for episode_file in new_episodes_files:
            episode_no_user = episode_file.replace("[Erai-raws] ", "")
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
            #print(f"{rating}: {episodes} -> NULL")


def extract_number(f):
    s = re.findall("\d+$", f)
    return (int(s[0]) if s else -1, f)


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


if __name__ == '__main__':
    main()
