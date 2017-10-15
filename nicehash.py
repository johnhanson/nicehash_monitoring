import json
import urllib.request
import time
import datetime
import threading
import os

# my libraries
import algo
api_readonly = ""
address = ""

with open('readonly_api.txt', 'r') as f:
    api_readonly = f.readline().strip()
with open('address.txt', 'r') as f:
    address = f.readline().strip()

def read_url(url):
    return json.loads(urllib.request.urlopen(url).read().decode("utf-8"))

def get_api_version():
    return read_url("https://api.nicehash.com/api")

def get_global_stats():
    return read_url("https://api.nicehash.com/api?method=stats.global.current")

def pretty_print(json_str):
    print(json.dumps(json_str, indent=4))

def acceptable_api_ver():
    curr_ver = get_api_version()['result']['api_version']
    known = '1.2.6'
    return(curr_ver == known)

def unix_to_human(timestamp):
    return(datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S'))

if not acceptable_api_ver():
    quit()

def sufficient_elapsed_time(algorithm_name, filename):
    time_s = algo.algo_to_refresh_rate(algorithm_name) # time in seconds
    with open(filename, "rb") as file:
        # if the file is empty then we want to immediatly log 
        # (open will create a file if one doesn't exist)
        filesize = os.path.getsize(filename)
        if filesize == 0:
            return True
        # the file contains at least two lines (header + data), unless someone fucked it up manually
        last_line = get_last_line(file)
        # we only want the first csv value (which is the unix timestamp)
        latest_timestamp = last_line.partition(",")[0]
        #print(latest_timestamp)
        update_time = int(latest_timestamp) + time_s
        if update_time < time.time():
            #print ("Because the next update time of " + str(update_time) + " is past, cuz now is " + str(int(time.time())) + " actually update the file " + filename)
            return True
        else: 
            #print ("Because the next update time of " + str(update_time) + " has not past, cuz now is " + str(int(time.time())) + " don't update the file " + filename)
            return False

# SO magic: https://stackoverflow.com/a/18603065
def get_last_line(file):
    first = file.readline()                 # Read the first line.
    file.seek(-2, os.SEEK_END)              # Jump to the second last byte.
    while file.read(1) != b"\n":            # Until EOL is found...
        file.seek(-2, os.SEEK_CUR)          # ...jump back the read byte plus one more.
    return file.readline().decode("utf-8")  # Read last line. and convert to string


class algorithm_thread (threading.Thread):
    def __init__(self, algorithm_number, current_stats):
        threading.Thread.__init__(self)
        self.algorithm_number = algorithm_number
        self.algorithm_name = algo.num_to_algo(self.algorithm_number)
        self.current_stats = current_stats
        self.refresh_rate = algo.algo_to_refresh_rate(self.algorithm_name)


    def run(self):
        filename = "logs\\" + self.algorithm_name + ".txt"
        if not sufficient_elapsed_time(self.algorithm_name, filename):
            quit()
        
        print("running:", self.algorithm_name)
        
        
        for algorithm in self.current_stats['result']['stats']:
            # only expand the one algorithm this thread wants
            if algo.num_to_algo(algorithm['algo']) == self.algorithm_name:
                with open(filename, "a") as file:
                    # need to set a flag if the file is empty to put the headers up top
                    filesize = os.path.getsize(filename)
                    #print("the filesize is " + str(filesize))
                    write_headers = False
                    if filesize == 0:
                        #print(filename + " is empty! going to write headers now")
                        write_headers = True
                    #print("writing data to: " + filename)
                
                    data_str = str(int(time.time())) + "," + unix_to_human(time.time()) + "," # the first line after the headers
                    header_str = "unix,time,"
                    for element in algorithm:
                        """
                        here is where I would use a case statement
                        IF PYTHON HAD ONE
                        
                        https://bitcointalk.org/index.php?topic=2009353.msg20112410#msg20112410
                        >profitability_above_ltc : "8.27" - profitability above what?
                        that's a damn good question you have there cTnko. wish I knew
                        """
                        
                        if element == 'profitability_above_ltc':
                            data_str = data_str + algorithm[element] + ","
                            header_str = header_str + element + ","
                        elif element == 'price':
                            data_str = data_str + algorithm[element] + "BTC/" + algo.num_to_speed(algorithm['algo']) + ","
                            header_str = header_str + element + ","
                        elif element == 'profitability_ltc':
                            data_str = data_str + algorithm[element] + ","
                            header_str = header_str + element + ","
                        elif element == 'profitability_above_btc':
                            data_str = data_str + algorithm[element] + ","
                            header_str = header_str + element + ","
                        elif element == 'profitability_btc':
                            data_str = data_str + algorithm[element] + ","
                            header_str = header_str + element + ","
                        elif element == 'profitability_above_eth':
                            data_str = data_str + algorithm[element] + ","
                            header_str = header_str + element + ","
                        elif element == 'profitability_eth':
                            data_str = data_str + algorithm[element] + ","
                            header_str = header_str + element + ","
                        elif element == 'speed':
                            data_str = data_str + algorithm[element] + algo.num_to_speed(algorithm['algo']) + ","
                            header_str = header_str + element + ","
                        elif element == 'algo':
                            # do nothing.
                            data_str = data_str
                            header_str = header_str
                        else:
                            data_str = data_str + "UNKNOWN ELEMENT INSIDE ALGORITHM " + element  + ","
                            header_str = header_str + "UNKNOWN ELEMENT INSIDE ALGORITHM " + element  + ","
                        # now that we're done processing through all the data, we can finally write to disk.
                        #print("writing to disk!")
                    if write_headers:
                        #print("writing the headers")
                        file.write(header_str + "\n")
                    file.write(data_str + "\n")
                    #print("done writing the data")
            #print(self.algorithm_name + " got finished going through it for time number " + str(i))
        
            
        print(self.algorithm_name + " IS DONE!")


def main():
    threads = []
    global_stats = get_global_stats()
    while True:
        all_algo = algo.get_algo()
        for algos in all_algo:
            thread = algorithm_thread(algos, global_stats)
            thread.start()
            threads.append(thread)
        
        for t in threads:
            t.join()
        # every 60 seconds
        print(unix_to_human(time.time()) + " sleeping......\n")
        time.sleep(60)
    
    print("DONE WITH MAIN THREAD")


if __name__ == '__main__':
    main()