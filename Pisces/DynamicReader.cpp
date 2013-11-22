#include <iostream>
#include <stdio.h>
#include <fstream>
#include <string>
#include <stack>
#include <cstring>
#include <unordered_map>
#include "DynamicReader.h"

using namespace std;

unordered_map<string, int> parse_log(string logfile)
{	
	unordered_map<string, int> funcMap;
	std::stack<string> functionStack;
	ifstream infile;
	ofstream outfile;
	const char * fname = logfile.c_str();
	string currline;
	infile.open(fname);
	outfile.open("parsedLog.log");
	while(!infile.eof())
	{
	getline(infile, currline);
	cout<<"current line is: " << currline << " and string length is " << currline.length() << endl;
	if(currline.compare("return") != 0)
		{
		unordered_map<string, int>::const_iterator got = funcMap.find(currline);
		if(got==funcMap.end())
			{
			funcMap.insert(make_pair(currline,1));
			//cout<<"adding: " << currline << " to map" << endl;
			}
		else
			{
			int newCount = got->second + 1;
			funcMap[currline] = newCount;
			}
		functionStack.push(currline);
		}
	else
		{
		string toFunc = functionStack.top();
		functionStack.pop();
		string fromFunc = functionStack.top();
		outfile << fromFunc << " " << toFunc << "\n";
		}
	}
	infile.close();
	outfile.close();
	funcMap.erase("");
	return funcMap;	
}

/*
int main(void)
{
	unordered_map<string, int> functionMap;
	functionMap = parse_log("test.log");
	for(auto& x: functionMap)
		cout<< x.first << ": " << x.second << endl;
}
*/
