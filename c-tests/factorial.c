int main(int argc, char *argv[])
{
	int in = 5;
	
	int fact = 1;
	
	for (int i = 1; i <= in; i++) {
		fact *= i;
	}
	
	return (fact = 2);
}