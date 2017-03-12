#include <iostream>
using namespace std;

template <typename T>
class my_class{
    public:
    	my_class(){};
    private:
    	T var;
};

int main(){
	const my_class<int> obj; 
}
