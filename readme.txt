1. This script is used to scrape creators data from binance live.It uses python,pandas and selenium to do the job.
2. The script is divided into two functions the first function convert_followers_to_int converts the followers count which is in a string ex:18.2k to an integer 18,200.
3. The main function getStreamerData clicks into a live category and starts to get the creators data like followers, id, bio, and verified or not one creator after the other.
4. The main function tries to find a div next to the user name if the div is present then it means its a verified account else it is not.
5. Finally this data is converted into a df and the df is saved as a .csv.
6. This data was used by the marketing team to reach out to different creators based on their following for promotions.
8. You can check end result by downloading the streamers_data.xlsx file. 
