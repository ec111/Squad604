/*
Dynamic Reader

Dynamic Reader takes in the log file produced by Fish from the
log statements that were injected by CodeInjector.
With this input it creates an unorderedmap of pairs of functions
that call one another.
*/
#include <iostream>
#include <stdio.h>
#include <fstream>
#include <string>
#include <stack>
#include <cstring>
#include <unordered_map>
#include "DynamicReader.h"

using namespace std;

/*
  parse_log
  This method returns an unordered_map of the functions and occurences of each function
  from the log file generated by the injected code into Fish
*/
unordered_map<string, int> parse_log(string logfile)
{	
	unordered_map<string, int> funcMap;
	// stack is used to store the function call stack
	std::stack<string> functionStack;
	ifstream infile;
	ofstream outfile;
	const char * fname = logfile.c_str();
	string currline;
	infile.open(fname);
	//outfile.open("parsedLog.log");

  // for every line of the input file
	while(!infile.eof())
	{
    getline(infile, currline);
    // the line is not a return, then it is pushed onto the stack
    if(currline.compare("return") != 0)
    {
      // the function is inserted into the unordered_map if the given function 
      // does not exists in the current map, otherwise the count for that specific
      // function will be incremented once
      unordered_map<string, int>::const_iterator got = funcMap.find(currline);
      if(got==funcMap.end())
      {
        funcMap.insert(make_pair(currline,1));
      }
      else
      {
        int newCount = got->second + 1;
        funcMap[currline] = newCount;
      }
      functionStack.push(currline);
    }
    // otherwise if the line is returned, then a function is popped off the stack
    // at this point a linked pair can be generated from the function on top of the stack
    // and the function that was just popped off the stack
    else
    {
      string toFunc = functionStack.top();
      functionStack.pop();
      if(!functionStack.empty())
      {
        string fromFunc = functionStack.top();
        //outfile << fromFunc << " " << toFunc << "\n";
      }
    }
	}
	//close the files and erase the blank line at the end that was causing issues with seg fault
	infile.close();
	//outfile.close();
	funcMap.erase("");
	return funcMap;	
}

/*

int main(void)
{
	unordered_map<string, int> functionMap;
	functionMap = parse_log("log.txt");
	for(auto& x: functionMap)
		cout<< x.first << ": " << x.second << endl;
}
*/
