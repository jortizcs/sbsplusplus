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

    print 'Please wait...'
    R = anomaly_count.read_Rmatrix(r_day)
    C_list = anomaly_count.get_Cmatrix_list(set)
    anomalies = anomaly_count.count_sp_day(R, C_list, day, tb, threshold)

    print '---------------------------'
    print 'The total number anomalies in this time is: '
    print anomalies

    print 'Enter 1 to see the detail, enter 2 to exit'
    choice = int(raw_input())
    if choice == 1:
        anomaly_count.detail(R, C_list, day, tb, threshold)
    else:
        print 'Thank you!'
        exit()

