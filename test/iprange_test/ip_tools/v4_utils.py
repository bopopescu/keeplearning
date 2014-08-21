import os
import sys

def ip2long(ipstring):
    nums = [int(x) for x in ipstring.split('.')]
    return (nums[0]<<24) + (nums[1]<<16) + (nums[2]<<8) + nums[3]

def long2ip(integer):
    octets = []
    for i in range(4):
        octets.insert(0, str(integer & 0xFF))
        integer >>= 8
    return '.'.join(octets)

def get_network(ip_str, cidr):
    ip = ip2long(ip_str)
    cidr = int(cidr)
    submask = 0
    for i in range(32-cidr, 32):
        submask += 1 << i
    submask &= ip
    return submask

def get_boardcast(ip_str, cidr):
    network = get_network(ip_str, cidr)
    cidr = int(cidr)
    temp_var = 0
    for i in range(0, 32-cidr):
        temp_var += 1<<i
    boardcast = network | temp_var
    return boardcast

def get_intersection(rg_a, rg_b):
    list_new = rg_a + rg_b
    list_new.sort()
    start = list_new[1]
    end = list_new[2]
    if start >= rg_a[0] and end <= rg_a[1] and start >= \
    rg_b[0] and end <= rg_b[1]:
        return [start, end]
    return None

def get_difference(rg_a, rg_b):
    intersection = get_intersection(rg_a, rg_b)
    if intersection is not None:
        result = []
        if intersection == rg_a:
            return None
        if intersection[0] > rg_a[0]:
            result.append([rg_a[0],intersection[0]-1])
        if intersection[1] < rg_a[1]:
            result.append([intersection[1]+1, rg_a[1]])
        return result
    return [rg_a]


def to_cidr(smallip, bigip):
    rt_dict = []
    if smallip > bigip:
        return None
    low_pose = 32
    ip = smallip - 1
    while ip < bigip:
        #find lowest bit which is 1
        ip += 1
        for i in range(0, 32):
            if ip&(1<<i):
                low_pose = i
                break
        if low_pose is 0:
            rt_dict.append([ip, 32])
            continue
        for k in range(low_pose, 0, -1):
            suffix = (1 << k) -1
            high_bound = ip | suffix
            if high_bound == bigip:
                rt_dict.append([ip, 32-k])
                return rt_dict
            elif high_bound < bigip:
                rt_dict.append([ip, 32-k])
                ip = high_bound
                break
            else:
                continue
        if bigip == ip:
            rt_dict.append([bigip, 32])
    return rt_dict

def range2IP(smallip, bigip):
    rt_list = []
    if smallip == bigip:
        rt_list.append([long2ip(smallip), long2ip(bigip)])
        return rt_list
    base = 0xff
    var = smallip
    x = 0
    #count smallip zero
    for n in range(4):
        zero = smallip & (base<<(n*8))
        if zero == 0:
            x += 1
        else:
            break
    #pretreatment
    if x is not 0:
        for i in range(x, 0, -1):
            var_board = var | ((base+1)**i-1)
            if var_board >= bigip:
                x = i - 1
                break
    while x < 4:
        x += 1 
        var_board = var | ((base+1)**x -1)
        if var_board == bigip:
            rt_list.append([long2ip(var), long2ip(bigip)])
            return rt_list
        if var_board < bigip:
            rt_list.append([long2ip(var), long2ip(var_board)])
            var = var_board + 1
            continue
        if var_board > bigip:
            break
    while x > 0:
        suffix = ((base+1)**(x-1)-1)
        if (bigip & suffix) == suffix:
            rt_list.append([long2ip(var), long2ip(bigip)])
            break
        big_net = ((bigip >> ((x-1)*8))) << ((x-1)*8)
        if var == big_net:
            x -= 1
            continue
        if x is 1:
            rt_list.append([long2ip(var), long2ip(big_net)])
        else:
            rt_list.append([long2ip(var), long2ip(big_net-1)])
        if bigip == big_net:
            rt_list.append([long2ip(big_net), long2ip(bigip)])
            break
        var = big_net
        x -= 1
    return rt_list

def list_sort(range_list):
    result_dict = sorted(range_list, key = lambda x:x[0])
    return result_dict

def combine(range_list):
    r_list = list_sort(range_list)
    result = []
    length = len(range_list)
    for i in range(length-1):
        if r_list[i+1][0] <= r_list[i][-1] \
        and r_list[i+1][-1] <= r_list[i][-1]:#in
            r_list[i+1][0] = r_list[i][0]
            r_list[i+1][-1] = r_list[i][-1]
            r_list[i] = []
        elif r_list[i+1][0] <= r_list[i][-1]+1 \
        and r_list[i+1][-1] > r_list[i][1]:
            r_list[i+1][0] = r_list[i][0]
            r_list[i+1][-1] = r_list[i+1][-1]
            r_list[i] = []
        else:
            result.append(r_list[i])
    result.append(r_list[-1])
    return result

if __name__ == "__main__":
    print long2ip(ip2long('0.255.243.0'))