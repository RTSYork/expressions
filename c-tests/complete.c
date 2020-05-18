typedef int int_type;

struct a_struct {
	int a;
	int b;
};

union a_union {
	int a;
	int b;
};

#pragma a_pragma

int a;
unsigned long b = 0;
int *c;
char arr[5] = "test";

int dbl(int a, ...) {
	return a * 2;
}

int main(void) {
	a = 1 + 2;
	b = dbl(a);

	if (a < 1) {
		return 1;
	}

	while (0) {
		a++;
		continue;
	}

	do {
		a--;
	} while (0);

	for (int i = 0; i < 10; i++) {
		a += 2;
	}

	lab: a = 1;
	goto lab;

	struct a_struct s;
	struct a_struct *sp = &s;
	s.a = 1;
	sp->b = 2;

	switch (a) {
	case 1:
		b = 1;
		break;
	case 2:
		b = 2;
		break;
	default:
		b = 0;
	}

	a = b ? 1 : 2;

	a += (int)10;

	for(;;);

	int c = a, b;

	return 0, 1;
}
