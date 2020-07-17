#include<iostream>
#include<cmath>
#include<vector>
#include<fstream>
#include<string>
using namespace std;
int main()
{
	int b, c, i, j, n, m;
	//	double summa;
	double inta, intb, a;
	double summax = 0, summay = 0, summax2 = 0, summaxy = 0;
	string s;
	vector <double> func1;
	vector <double> func2;
	vector <double> func3;
	vector <double> func4;
	vector <string> timer;
	vector <int> vectstart;
	vector <int> vectend;
	ifstream file;
	file.open("test1.txt");
	//for (i = 0; i < 9; i++)
	//	file >> s;
	getline(file, s);
	i = 1;
	while (!file.eof())
	{
		file >> s;
		file >> a;
		timer.push_back(s);
		func1.push_back(a);
		//	func4.push_back(i);
		summax = summax + i;
		summax2 = summax2 + i * i;
		summay = summay + a;
		summaxy = summaxy + a * i;
		i++;
	}
	i--;
	summax = summax - i;
	summax2 = summax2 - i * i;
	summay = summay - a;
	summaxy = summaxy - a * i;
	n = i - 1;
	//cout << summax << " " << summay << " " << summax2 << " " << summaxy<<endl;
	//a*summax2+b*summax=summaxy
	//a*summax+b*n=summay

	intb = (double)(summaxy * summax - summax2 * summay) / (summax * summax - n * summax2);
	inta = (double)(summay - n * intb) / summax;
	//cout << inta << " " << intb<<endl;
	for (i = 0; i < n; i++)
	{
		func2.push_back(inta * i + intb);
		func3.push_back(func2[i] - func1[i]);
		//cout << func1[i] << " " << func3[i]<<endl;
	}

	/*for (i = 0; i < n; i++)
	{
		for (j = 1; j < n - 1; j++)
		{
			if (func3[j] > func3[j - 1])
			{
				swap(func3[j], func3[j - 1]);
				swap(func4[j], func4[j - 1]);
			}
		}
	}*/
	double diff, maxdiff = 0;

	m = 0;
	for (i = 0; i < n - 120; i++)
	{
		diff = 0;
		vectstart.push_back(0);
		vectend.push_back(0);
		if (func3[i] > 0)
		{
			for (j = i; j < i + 120; j++)
			{
				if (func3[j]<0 && abs(func3[i] - func3[j])>diff)
				{
					diff = abs(func3[i] - func3[j]);
					vectstart[m] = i;
					vectend[m] = j;
				}

			}

		}

		m++;
		func4.push_back(diff);
		if (maxdiff < diff)
			maxdiff = diff;
	}
	//cout << vectstart.size() << " " << vectend.size() << " " << func4.size() << endl;
	for (i = 0; i < vectstart.size(); i++)
		if (func4[i] < maxdiff / 2)
		{
			vectstart.erase(vectstart.begin() + i);
			vector<int>(vectstart).swap(vectstart);
			vectend.erase(vectend.begin() + i);
			vector<int>(vectend).swap(vectend);
			func4.erase(func4.begin() + i);
			vector<double>(func4).swap(func4);
			i--;
		}
	vector <int> start;
	vector <int> end;
	start.push_back(vectstart[0]);
	for (i = 0; i < vectstart.size() - 1; i++)
	{
		if (vectstart[i + 1] != vectstart[i] + 1)
		{
			end.push_back(vectend[i]);
			start.push_back(vectstart[i + 1]);
		}
	}
	end.push_back(vectend[vectend.size() - 1]);
	string razd = "=====================================================================================";
	int result = func1[0], pk;
	int zapravleno = 0, potracheno = 0;
	cout << "In beggining: " << func1[0] << endl << razd << endl;
	pk = func1[0] - func1[start[0]];
	cout << "spent before refueling: " << pk << endl;
	potracheno = potracheno + pk;
	result = result - pk;
	for (i = 0; i < end.size(); i++)
	{
		pk = abs(func1[end[i]] - func1[start[i]]);
		cout << "refueling " << i + 1 << ": " << pk <<"\t time:("<<timer[start[i]]<<", "<<timer[end[i]]<<")"<< endl << razd << endl;
		zapravleno = zapravleno + pk;
		result = result + pk;

		if (i < end.size() - 1)
		{
			pk = func1[end[i]] - func1[start[i + 1]];
			cout << "spent before refueling: " << pk << endl;
			result = result - pk;
			potracheno = potracheno + pk;
		}
		else
		{
			pk = func1[end[i]] - func1[func1.size() - 1];
			cout << "spent in end: " << pk << endl;
			potracheno = potracheno + pk;
			result = result - pk;
		}
	}
	cout << endl << "Result: " << result << "\t Left in end: " << func1[func1.size() - 1] << "\t Total refueled: " << zapravleno << "\t Total spent: " << potracheno << "\t Total refueling: " << end.size() << endl;
	file.close();
}