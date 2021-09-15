import sys
sys.path.append('C:\Mealkit_Recommendation')

from market_kurly.kurly_scrapping import Kurly_Scrapping

kurly = Kurly_Scrapping()

kurly.land_first_page()