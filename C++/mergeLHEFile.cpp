// g++ -Wall -o mergeLheFile mergeLheFile.cpp

#include <iostream>
#include <fstream>



int main(int argc, char** argv)
{
  if(argc != 3)
  {
    std::cout << ">>>splitLheFile.cpp::Usage:   " << argv[0] << "   initialFile.lhe   fileToAdd.lhe" << std::endl;
    return -1;
  }
  
  char* initialFileName = argv[1]; 
  char* fileToAddName = argv[2]; 
  
  std::cout << "initialFileName = " << initialFileName << std::endl;
  std::cout << "fileToAddName = " << fileToAddName << std::endl;
  
  
  
  // open lhe file
  std::ifstream initialFile(initialFileName, std::ios::in);
  std::ifstream fileToAdd(fileToAddName, std::ios::in);
  std::ofstream outFile("out.lhe", std::ios::out);
  
  std::string line;
  std::string line2;
  bool writeEvent = false;
  int eventIt = 0;
  
  while(!initialFile.eof())
  {
    getline(initialFile, line);
    
    if( line == "</LesHouchesEvents>" )
    {
      while(!fileToAdd.eof())
      {
        getline(fileToAdd, line2);      
        
        // decide whether to skip event or not 
        if( line2 == "<event>" )
        {
          ++eventIt;
          writeEvent = true;
        }
        
        
        // write line to outFile
        if(writeEvent == true)
          outFile << line2 << std::endl;
        
        
        // end of event
        if( line2 == "</event>" )
          writeEvent = false;
      }
    } 
    
    outFile << line << std::endl;
  }
  
  
  std::cout << "Added " << eventIt << " events from file " << fileToAddName << " to file " << initialFileName << std::endl;
  return 0;
}
