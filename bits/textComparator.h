#ifndef TEXTCOMPARATOR_H
#define TEXTCOMPARATOR_H

#include <string>
#include <fstream>
#include <cassert>

using namespace std;

struct TextComparator
{
    string outputFName;
    ofstream &out;

    TextComparator(string fname, ofstream &o) : outputFName(fname), out(o) {}
    
    ~TextComparator()
    {
        out.close();
        std::ifstream in1(outputFName);
        std::ifstream in2("output.txt");
        string line1;
        string line2;
        while(getline(in1, line1))
        {
            if (!getline(in2, line2)) // PROBLEM: files aren't same length
            {
                assert(0);
            }
            
            if (line1 != line2) // PROBLEM: lines aren't the same
            {
                assert(0);
            }
        }
    }
};

#endif