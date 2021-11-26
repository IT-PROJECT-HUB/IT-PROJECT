#include <iostream>
#include <process.h>

int main(int argc, char* args[])
{
	using namespace std;
	cout << "7-zip archiving..." << endl;
	if (argc > 1)
	{
		_spawnlp(P_WAIT, "C:\\Program Files\\7-Zip\\7z.exe", "\"C:\\Program Files\\7-Zip\\7z.exe\"", "a", "result.7z", args[1], NULL);
		cout << "Done!" << endl;
		system("pause");
	}
	else
		cout << "No file to compression..." << endl;
}
