package main
import "fmt"
// import "math/rand"

const (
    int32max = (1<<31) -1
)

func seedrand(x int32) int32 {
	const (
		A = 48271
		Q = 44488
		R = 3399
	)

	hi := x / Q
	lo := x % Q
	x = A*lo - R*hi
	if x < 0 {
		x += int32max
	}
	return x
}

func main(){
    var xx int32;
    xx = -1
    fmt.Printf("%d\n", uint64(xx));
    // rand.Seed(30);
    // for i:=0; i<1000; i++{
    //     fmt.Printf("%d\n", rand.Intn(2023));
}
