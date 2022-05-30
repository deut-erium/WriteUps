from gmpy2 import iroot
n =102775814277835851799212072411451153125581751948703981931225275130311351091488627735780737511014295604852105321540950670615414262390789259544774351385875632749370076758721685499409700125665154334688524128388873864019227708029952609796372848318017496098902680819026565214414650901501467063204051423025612213679
e =100721465514806669050993883220221035922420749271501971549630927095261306951267013077618465597789524683696043049963724939982254816398323920501236610282938418850156772344184059388104031453374834393907183004860329967786049390729199042209066226603276484868663988379138231263328642164467919740230210328397521110272
ct =55889516016819520230362162551277479130446271307637280074721321200107487592857859338195870955263783699846154419705783242126240701572290107453292528281784347936660522829144917957611499465315945070914821823392594076278095378949188748825934721900493032624225181273857480489283982160777732325351739831819307071657

facs=[1962985659049224511332677493428661566121762428734174192248289261057229816924911547344337613406671073029689056114433098168911521003505206771817920162516245121734637342682002398242634109522079399337521843035777766664963499871453492606346471930182864455896751666140785399679943552579186388451464284819,113, 7829, 2609953]


for t in range(1,100000):
    b = e-t-n*t
    D = b**2 - 4*t*(45*e+n*t-1)
    d,psq = iroot(D,2)
    if psq:
        print(d,t)