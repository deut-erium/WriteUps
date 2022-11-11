use rand::{Rng,SeedableRng};
use rand::rngs::StdRng;
use std::fs;
use std::io::Write;
use std::time::SystemTime;
use std::io;
use std::io::prelude::*;
use std::fs::File;

fn get_rng() -> StdRng {
    let seed = SystemTime::now()
        .duration_since(SystemTime::UNIX_EPOCH)
        .expect("Time is broken")
        .as_secs();
    println!("{}",seed);
    return StdRng::seed_from_u64(seed);
}

fn rand_xor(input : String) -> String {
    let mut rng = get_rng();
    return input
        .chars()
        .into_iter()
        .map(|c| format!("{:02x}", (c as u8 ^ rng.gen::<u8>())))
        .collect::<Vec<String>>()
        .join("");
}

fn bf_seed(seed: u64,input: String) -> String {
    let mut rng = StdRng::seed_from_u64(seed);
    return input
        .chars()
        .into_iter()
        .map(|c| format!("{:02x}", (c as u8 ^ rng.gen::<u8>())))
        .collect::<Vec<String>>()
        .join("");
}

fn main() -> std::io::Result<()> {
    /*
    let flag = fs::read_to_string("flag.txt")?;
    let xored = rand_xor(flag);
    println!("{}", xored);
    let mut file = fs::File::create("out.txt")?;
    file.write(xored.as_bytes())?;
    */
    //let mut f = File::open("out.txt")?;
    //let mut input = f.bytes();
    let mut input = fs::read_to_string("out.txt")?;
    for i in 1..100{
        let xored = bf_seed(1618990085-i,input.clone());
        println!("{}",xored);
    }
    Ok(())
}
