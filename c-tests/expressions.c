int b, c;
int d[2];

int main(int argc, char *argv[])
{
	int a = 1 + 2;
	b = a + 3 + 4 + 5;
	c = (a * b++ + 6 - 7) / 8;
	a += 1;
	++b;
	a = b + c;
	d[0] = 1;
	*(d + 1) = 2;
	return a = 1, b = 2;

	a = b++;
}
