# def convert_followers_to_int(followers_text):
#     multiplier = 1
#     if 'k' in followers_text:
#         multiplier = 1000
#         followers_text = followers_text.replace('k', '')
#     elif 'm' in followers_text:
#         multiplier = 1000000
#         followers_text = followers_text.replace('m', '')
#     # Remove any commas or dots
#     followers_text = followers_text.replace(',', '')
#     followers_count = float(followers_text) * multiplier
#     return int(followers_count)

# count =convert_followers_to_int("2.1k")

# print(count)


arr = [1, 2, 3]

def increse():
    count = 0
    for a in arr:
        count += 1
    # print(count)
    return count

def printIam():
    count = increse()
    if count == 3:
        print(f"I am {count}")      

increse()
printIam()