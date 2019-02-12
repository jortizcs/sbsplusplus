import anomaly_count

if __name__ == '__main__':
    print'-------------------------------------------'
    print 'Welcome to the building anomaly detection system'
    print 'Please choose a building:'
    print '1. Rice'
    set = raw_input()
    print 'Please choose the day you want measure (1-6):'
    day = int(raw_input())
    print 'Please choose the time bin in this day (0-3):'
    tb = int(raw_input())
    print 'Please choose the reference type:'
    print '1. 1day reference'
    print '2. 2day reference'
    print '3. 3day reference'
    r_day = int(raw_input())
    print 'Please choose the threshold (1-20):'
    threshold = int(raw_input())

    print 'Please choose the search option:'
    print '1. Cell'
    print '2. Vector'
    search_op = int(raw_input())

    print 'Please wait...'
    R = anomaly_count.read_Rmatrix(r_day)
    C_list = anomaly_count.get_Cmatrix_list(set)
    abn_sensors = anomaly_count.count_interface(R, C_list, day, tb, threshold, search_op)
    num_of_anomalies = len(abn_sensors)

    print '---------------------------'
    print 'The total number anomalies in this time is: '
    print num_of_anomalies

    print 'Press 1 to check the anomalies:'
    check = int(raw_input())
    anomaly_count.anomaly_check(R, abn_sensors, day, tb)

    print 'Thank you!'
    exit()

