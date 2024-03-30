1. This script is used to scrape and create a data frame of creators data from binance live.It uses python,pandas and selenium to do the job.
2. The script is divided into two functions the first function "convert_followers_to_int", converts the followers count which are strings ex:18.2k to an integer value 18,200.
3. The main function "getStreamerData", opens the browser, navigates to binance-live, clicks into a live category and starts to get the creators data like followers, id, bio, and verified or not, one creator after the other.
4. The main function gets checks weather a profile is verified or not by finding a div next to the user name, if the div is present then this means its a verified account, else it is not.
5. Finally this data is converted into a data frame and the df is saved as a .xlsx file.
6. This data was used by the marketing team to reach out to different creators based on their following for promotions.
8. You can check end result by downloading the streamers_data.xlsx file. 
