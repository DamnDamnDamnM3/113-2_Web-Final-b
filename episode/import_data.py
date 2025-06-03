import json
# import os
# import django
from django.core.exceptions import ObjectDoesNotExist

# Setup Django environment
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
# django.setup()

from episode.models import Season, Episode

# Load JSON data
with open('episode/json_data/title.json', 'r', encoding='utf-8') as f:
    titles = json.load(f)

with open('episode/json_data/en_plot.json', 'r', encoding='utf-8') as f:
    en_plots = json.load(f)

with open('episode/json_data/tw_plot.json', 'r', encoding='utf-8') as f:
    tw_plots = json.load(f)

# Populate the models
for key, title in titles.items():
    season_num, ep_num = key.strip('[]').split(',')
    print (season_num, ep_num)
    season, created = Season.objects.get_or_create(season_number=season_num)
    
    if not created:
        season.save()

    en_plot = en_plots.get(key, "")
    tw_plot = tw_plots.get(key, "")

    print (en_plot, tw_plot)
    
    episode, created = Episode.objects.get_or_create(
        season = season,
        ep_number = ep_num,
        defaults={'ep_title': title, 
                  'eng_plot': en_plot, 
                  'tw_plot': tw_plot}
    )
    
    # Update plots if the episode already exists
    if not created:
        episode.eng_plot = en_plot
        episode.tw_plot = tw_plot
        episode.save()

print("Data populated successfully!")

# exec(open('episode/import_data.py').read())
# Episode.objects.all().delete()

# 刪除所有Season資料
# Season.objects.all().delete()
