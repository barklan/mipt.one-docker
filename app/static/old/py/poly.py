def polyhash(s, p, m):
    lenm = len(s)
    h = pow(p,lenm-1)%m
    ans = 0
    result = []
    for i in range(lenm): # preprocessing
        ans = (p*ans+ord(s[i]))%m
    return ans
