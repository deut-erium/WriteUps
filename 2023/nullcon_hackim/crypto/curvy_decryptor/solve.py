from ec import *
from utils import *
import pwn
from tqdm import tqdm
from Crypto.Util.number import *
from Crypto.Cipher import AES
from sympy.ntheory.modular import crt
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = -3
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
curve = EllipticCurve(p, a, b, order=n)
G = ECPoint(
    curve,
    0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
    0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)

HOST, PORT = "52.59.124.14", 10005
REM = pwn.remote(HOST, PORT)

REM.recvline()  # My public key is:
pubkey = REM.recvline().strip()[6:-1].split(b',')
P_a = ECPoint(curve, int(pubkey[0]), int(pubkey[1]))

REM.recvline()  # Good luck decrypting this cipher.
B_text = REM.recvline().strip()[6:-1].split(b',')
B = ECPoint(curve, int(B_text[0]), int(B_text[1]))

c_text = REM.recvline().strip()[6:-1].split(b',')
c = ECPoint(curve, int(c_text[0]), int(c_text[1]))

flag2_enc = bytes.fromhex(REM.recvline().strip().decode())

# I will decrypt anythin as long as it does not talk about flags.
REM.recvline()

# d_a = int.from_bytes(Random.get_random_bytes(20))


def decrypt(B: ECPoint, c: ECPoint, d_a: int):
    if B.inf or c.inf:
        return b''
    return long_to_bytes((c - (B * d_a)).x)


def get_decryption(B, c):
    # return 100,decrypt(B,c,d_a)
    REM.sendline("{},{}".format(B.x, B.y))
    REM.sendline("{},{}".format(c.x, c.y))
    status = REM.recvline()
    print(status)
    if b'cannot afford' in status:
        return -1, None
    balance = int(REM.recvline().strip().split(b': ')[-1])
    return balance, bytes.fromhex(status.strip()[6:-1].decode())


bal, BG = get_decryption(B - G, c)
BG_int = int.from_bytes(BG)
y = modular_sqrt(BG_int**3 + a * BG_int + b, p)
point_BG = ECPoint(curve, BG_int, y)
print(int.to_bytes((point_BG - P_a).x, 32, 'big'))


def get_invalid_curves(cutoff=10**5):
    factors = {}
    total = 1
    i = 0
    while total < p * 2:
        try:
            E = EllipticCurve(GF(p), [a, i])
            order = E.order()
            n_facs = order.factor()
        except ArithmeticError:
            i += 1
            continue
        for prime, power in n_facs:
            if prime > cutoff:
                break
            if prime in factors:
                if factors[prime][0] < power:
                    gen = E.gen(0) * (order // prime)
                    # total *= prime**(power-factors[prime][0])
                    factors[prime] = [power, int(gen[0]), int(gen[1]), i]
            else:
                gen = E.gen(0) * (order // prime)
                factors[prime] = [power, int(gen[0]), int(gen[1]), i]
                # total *= prime**(power)
                total *= prime
        print(i, total)
        i += 1
    return factors

# factor, power, gen.x, gen.y, b_i


invalid_curves = {
    7: [1, 7494160963166719022445789448670075468300539216220596044581361034311676798234, 98511591492536111584332615786483658886888663084020823615343609813895225923287, 0],
    71: [1, 47689891150662520216418276050802771367044708366511766907543187521601344242001, 76986723505258444611874235435887405018513758524921757765033540214285112109625, 1],
    823: [1, 101591078169875595753109991494905506967978136240961172388509275621325253165256, 10303457253039461887297603877250453486351456285884301634668455036581356870325, 1],
    1229: [1, 91709248688928381574970306879959143256779911355970659117798234761550615769703, 85856020107303390216619790339131383987393998107943546966635616939179964220668, 1],
    7489: [1, 69497610789705595174058737106242513100950130190920702467431032172354669590563, 43000989776377667520933328800675765150040604546037676698173382008099239610730, 1],
    30203: [1, 27140306769124364253212826889951250714782929180685455599284687702513066987645, 27465668374540052358785326933904597047991904030378513297677516281690992773738, 1],
    3: [2, 79692280239272980873245387831874823476097665365069163558817570386218657526967, 15885657487155030912288031888128427124936813080859472376494663130798867119982, 12],
    13: [1, 44238399751822344629155927349410921734336660036385908812849527496419061724190, 111209137730801733774021088162408683888753865848469665403753663663899601005809, 3],
    37: [1, 6829338390266237482283310246665103308891228336319477318479644522260556056309, 74701668267551028200304338837410580676774474001240882947774298643661074111881, 3],
    97: [1, 109352438132789597676269849271161933029115963700376783044214805643475162939438, 40494199582133551395560104592591896448854412368997470369685720658455096277720, 3],
    113: [1, 24758423058742208238204864443231318968571918830166822957638906079202832915346, 64680694216633390865014362020707904150333340051904806580803858267985332824228, 3],
    19: [1, 108657251488837839710095894743866739052486880271258033613510419634191398226376, 8593905934316229092193387452437731577526088690676465668457131094758391852209, 4],
    179: [1, 83115631016490504822328655777895864162660782325660359674792065332260812135544, 35707141486916353816358123900356888673488260709581875628819622187261352405569, 4],
    13003: [1, 69994388431307856080322572731970917270151067511018517619530568914812259046195, 51645889020375608054366335957352074257130320976341249224010343992676177045239, 4],
    2447: [1, 107091037109612570995136294213336682923913717986054179094643922074841981090569, 38297847735446351346601186761335949464902974429727652825128988635682228100545, 5],
    5: [2, 30463586456259052716174121724723788478797318939762291523651966151233767925799, 14521026652335616630611219515390291411023400641948957680811406721043438902186, 12],
    4003: [1, 69634612360547639692978050736475584000001950346963254134893659331303767659709, 7267690154676021708711188497795027916155791784399213931355851351510639163175, 6],
    16033: [1, 80150849770701280770379260802876332257245651607220436873841708569583336291111, 67454443034144602807761039494179913732280388550455172486599878108995578176702, 6],
    1151: [1, 4942947285962241518079147671001480777229821084370946279070977308149340420785, 16048516228456466259745940658231903287363041924322695524263376011778714624389, 7],
    7103: [1, 110323527740892356276833844768860449554291010208201255792825053403232044044793, 34702628194678317337541067016532288256370093140368313590333192034888987762792, 7],
    81173: [1, 41965847134675666863089670621412699297207446259915277832939899605119013001686, 97595102592346869875749873612676528534971198259624427507680148771098555985918, 8],
    653: [1, 96946680343613920300091880607027973891460464096741803273170797219756170839615, 82843786165425711709725308210080928839669646246950072002603300248219042690214, 9],
    72337: [1, 16864673136043278693040185572303485743677125999233419976437302471094264721938, 39982110747848740588957884598316010802865483814669576940304708444368796141014, 9],
    17: [1, 9274144687945784364291903707116312659963917031850121885976057784793297477861, 86301980488975426887521079169756244075123784201450393961147458432303011672794, 10],
    251: [1, 22589597796365257246296758128505770638799961769310824687868041010311103597978, 22730375842099404560129412560882492093998724011749582473003682871994848593450, 10],
    19423: [1, 86763316696116146207846209443089376095966542281990071872698734124275764832625, 1497373281188841342082112917519408391664673991593710756225816313602284346637, 11],
    389: [1, 61737418306809996908630595437832052272700263892021361415640028314169193468679, 38812622012907358702971098652989910931710935180589252493039839244464470874161, 12],
    52183: [1, 20786893006200668135980517481305198967871522130773700571327256180224225598537, 38476450712159672989047119873673988596095516096648184067210103163599625447149, 12]}


def bruteforce(point, generator, order):
    for i in tqdm(range(order), desc=f"bruteforcing {order=}"):
        if point.y == (generator * i).y:
            return i


modulii = {}
for order, (power, gen_x, gen_y, b_i) in sorted(invalid_curves.items()):
    gen = ECPoint(curve, gen_x, gen_y)
    bal, BG = get_decryption(-gen, gen)  # gen*(da+1)
    BG_int = int.from_bytes(BG)
    y = modular_sqrt(BG_int**3 + a * BG_int + b_i, p)
    point_BG = ECPoint(curve, BG_int, y)

    bal, BG2 = get_decryption(-gen, gen * 2)  # gen*(da+2)
    BG_int2 = int.from_bytes(BG2)
    y2 = modular_sqrt(BG_int2**3 + a * BG_int2 + b_i, p)
    point_BG2 = ECPoint(curve, BG_int2, y2)
    if point_BG + gen == point_BG2:
        modulii[order] = bruteforce(point_BG, gen, order)
    elif point_BG - gen == point_BG2:
        modulii[order] = bruteforce(-point_BG, gen, order)
    elif -point_BG + gen == point_BG2:
        modulii[order] = bruteforce(-point_BG, gen, order)
    elif -point_BG - gen == point_BG2:
        modulii[order] = bruteforce(point_BG, gen, order)
    else:
        print("hmm")

mods, values = [], []
for i, v in modulii.items():
    mods.append(i)
    values.append((v - 1) % i)

d_a = crt(mods, values)[0]

key = long_to_bytes(
    (d_a >> (
        8 *
        16)) ^ (
            d_a & 0xffffffffffffffffffffffffffffffff))
print(AES.new(key, AES.MODE_ECB).decrypt(flag2_enc))
