const ips = Array.from({length: 34}, (_, i) => `${10 + i}.${(i*7+3)%256}.${(i*13+5)%256}.${(i*3+1)%256}`);
console.log(ips);
