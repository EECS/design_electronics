var K  = 1;
var fz = 20;
var fp = 40;

function linspace(a,b,n) {
    var every = (b-a)/(n-1),
        range = [];
    for (i = a; i < b; i += every)
        range.push(i);
    return range.length == n ? range : range.concat(b);
}

function logspace(a,b,n) {
    return linspace(a,b,n).map(function(x) { return Math.pow(10,x); });
}

function leadlag(f) {
    w = 2*math.pi*f;
    s = math.complex(0,w);
    wz = 2*math.pi*fz;
    wp = 2*math.pi*fp;
    var temp = math.multiply(K,math.multiply(math.divide(wp,wz),math.divide(math.add(s,wz),(math.add(s,wp)))));
    return temp;
};

function angle(f) {
    return math.atan2(f.im,f.re);
};

function deg2rad(deg) {
    return deg * math.pi / 180;
};

function rad2deg(rad) {
    return rad * 180 / math.pi;
};

function mag2db(mag) {
    return 20 * Math.log10(mag);
}

function db2mag(db) {
    return math.pow(10,db / 20);
}