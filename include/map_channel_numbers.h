#ifndef __map_channel_numbers_h__
#define __map_channel_numbers_h__

//----------------------------------------------------------------------------------------------------
// Map information for sicell (pad ID) and HGCROC pin
// key = globalId, value = pad ID or HGCROC pin (specified on map name)
// "CALIB" is replaced with the same pin number as its outer cell 
//----------------------------------------------------------------------------------------------------

std::map<int, int> map_SiCell_pad_full_wafer = {{0,36}, {1,26}, {2,35}, {3,25}, {4,8}, {5,17}, {6,16}, {7,7}, {9,6}, {10,15}, {11,5}, {12,13}, {13,34}, {14,33}, {15,23}, {16,24}, {18,14}, {20,4}, {21,12}, {22,3}, {23,11}, {24,2}, {25,1}, {26,10}, {27,9}, {29,21}, {30,31}, {31,22}, {32,32}, {33,19}, {34,29}, {35,20}, {36,30}, {39,46}, {40,58}, {41,47}, {42,59}, {43,44}, {44,57}, {45,56}, {46,45}, {48,74}, {49,88}, {50,87}, {51,73}, {52,71}, {53,86}, {54,72}, {55,85}, {57,70}, {59,69}, {60,84}, {61,68}, {62,83}, {63,43}, {64,42}, {65,55}, {66,54}, {68,67}, {69,82}, {70,66}, {71,81}, {72,52}, {73,41}, {74,53}, {75,40}, {78,165}, {79,177}, {80,151}, {81,166}, {82,178}, {83,188}, {84,198}, {85,189}, {87,179}, {88,167}, {89,168}, {90,153}, {91,137}, {92,123}, {93,138}, {94,152}, {96,154}, {98,155}, {99,139}, {100,140}, {101,125}, {102,126}, {103,111}, {104,110}, {105,95}, {107,109}, {108,93}, {109,124}, {110,108}, {111,94}, {112,79}, {113,80}, {114,65}, {117,121}, {118,135}, {119,136}, {120,150}, {121,107}, {122,106}, {123,91}, {124,122}, {126,120}, {127,104}, {128,89}, {129,105}, {130,76}, {131,75}, {132,90}, {133,60}, {135,62}, {137,61}, {138,48}, {139,49}, {140,37}, {141,92}, {142,78}, {143,77}, {144,63}, {146,38}, {147,27}, {148,28}, {149,18}, {150,39}, {151,64}, {152,50}, {153,51}, {156,99}, {157,98}, {158,115}, {159,114}, {160,96}, {161,97}, {162,113}, {163,112}, {165,127}, {166,128}, {167,141}, {168,142}, {169,130}, {170,145}, {171,144}, {172,129}, {174,143}, {176,157}, {177,156}, {178,169}, {179,170}, {180,180}, {181,190}, {182,181}, {183,191}, {185,171}, {186,172}, {187,158}, {188,159}, {189,192}, {190,193}, {191,182}, {192,183}, {195,100}, {196,101}, {197,116}, {198,117}, {199,146}, {200,132}, {201,147}, {202,131}, {204,102}, {205,103}, {206,119}, {207,118}, {208,148}, {209,134}, {210,133}, {211,149}, {213,163}, {215,162}, {216,164}, {217,175}, {218,176}, {219,160}, {220,173}, {221,161}, {222,174}, {224,186}, {225,187}, {226,196}, {227,197}, {228,195}, {229,184}, {230,185}, {231,194}};

std::map<int, int> map_HGCROC_pin_full_wafer = {{0,0}, {1,1}, {2,2}, {3,3}, {4,4}, {5,5}, {6,6}, {7,7}, {9,9}, {10,10}, {11,11}, {12,12}, {13,13}, {14,14}, {15,15}, {16,16}, {20,19}, {21,20}, {22,21}, {23,22}, {24,23}, {25,24}, {26,25}, {27,26}, {29,28}, {30,29}, {31,30}, {32,31}, {33,32}, {34,33}, {35,34}, {36,35}, {39,36}, {40,37}, {41,38}, {42,39}, {43,40}, {44,41}, {45,42}, {46,43}, {48,45}, {49,46}, {50,47}, {51,48}, {52,49}, {53,50}, {54,51}, {55,52}, {59,55}, {60,56}, {61,57}, {62,58}, {63,59}, {64,60}, {65,61}, {66,62}, {68,64}, {69,65}, {70,66}, {71,67}, {72,68}, {73,69}, {74,70}, {75,71}, {78,0}, {79,1}, {80,2}, {81,3}, {82,4}, {83,5}, {84,6}, {85,7}, {87,9}, {88,10}, {89,11}, {90,12}, {91,13}, {92,14}, {93,15}, {94,16}, {98,19}, {99,20}, {100,21}, {101,22}, {102,23}, {103,24}, {104,25}, {105,26}, {107,28}, {108,29}, {109,30}, {110,31}, {111,32}, {112,33}, {113,34}, {114,35}, {117,36}, {118,37}, {119,38}, {120,39}, {121,40}, {122,41}, {123,42}, {124,43}, {126,45}, {127,46}, {128,47}, {129,48}, {130,49}, {131,50}, {132,51}, {133,52}, {137,55}, {138,56}, {139,57}, {140,58}, {141,59}, {142,60}, {143,61}, {144,62}, {146,64}, {147,65}, {148,66}, {149,67}, {150,68}, {151,69}, {152,70}, {153,71}, {156,0}, {157,1}, {158,2}, {159,3}, {160,4}, {161,5}, {162,6}, {163,7}, {165,9}, {166,10}, {167,11}, {168,12}, {169,13}, {170,14}, {171,15}, {172,16}, {176,19}, {177,20}, {178,21}, {179,22}, {180,23}, {181,24}, {182,25}, {183,26}, {185,28}, {186,29}, {187,30}, {188,31}, {189,32}, {190,33}, {191,34}, {192,35}, {195,36}, {196,37}, {197,38}, {198,39}, {199,40}, {200,41}, {201,42}, {202,43}, {204,45}, {205,46}, {206,47}, {207,48}, {208,49}, {209,50}, {210,51}, {211,52}, {215,55}, {216,56}, {217,57}, {218,58}, {219,59}, {220,60}, {221,61}, {222,62}, {224,64}, {225,65}, {226,66}, {227,67}, {228,68}, {229,69}, {230,70}, {231,71}, {18,12}, {57,55}, {96,12}, {135,55}, {174,12}, {213,55} };

std::map<int, int> map_SiCell_pad_partial_wafer = { {24,107},{25,123},{26,124},{27,108},{20,75},{21,91},{22,89},{23,76},{28,126},{29,77},{0,85},{4,103},{8,-1},{59,32},{58,-1},{55,2},{54,10},{57,13},{56,-1},{51,31},{50,21},{53,1},{52,9},{115,-1},{114,173},{88,167},{89,180},{111,197},{110,155},{113,184},{112,172},{82,137},{83,151},{80,154},{81,139},{86,-1},{87,168},{84,136},{85,152},{3,86},{7,120},{108,140},{109,156},{102,196},{103,195},{100,182},{101,183},{106,207},{107,141},{104,205},{105,206},{39,57},{38,-1},{33,109},{32,92},{31,93},{30,61},{37,-1},{36,125},{35,142},{34,110},{60,33},{61,22},{62,23},{63,11},{64,3},{65,4},{66,12},{67,-1},{68,24},{69,14},{2,72},{6,119},{99,170},{98,171},{91,193},{90,181},{93,194},{92,203},{95,-1},{94,204},{97,185},{96,169},{11,88},{10,74},{13,105},{12,87},{15,122},{14,121},{17,-1},{16,106},{19,157},{18,90},{116,-1},{48,20},{49,30},{46,44},{47,-1},{44,56},{45,55},{42,58},{43,43},{40,45},{41,46},{1,71},{5,104},{9,73},{77,-1},{76,-1},{75,60},{74,48},{73,59},{72,47},{71,35},{70,34},{79,138},{78,153} };

std::map<int, int> map_HGCROC_pin_partial_wafer = { {24,23},{25,24},{26,25},{27,26},{20,19},{21,20},{22,21},{23,22},{28,27},{29,28},{0,0},{4,4},{8,8},{59,55},{58,54},{55,52},{54,51},{57,62},{56,53},{51,48},{50,47},{53,50},{52,49},{115,-1},{114,35},{88,10},{89,11},{111,32},{110,31},{113,34},{112,33},{82,4},{83,5},{80,2},{81,3},{86,8},{87,9},{84,6},{85,7},{3,3},{7,7},{108,29},{109,30},{102,23},{103,24},{100,21},{101,22},{106,27},{107,28},{104,25},{105,26},{39,36},{38,-1},{33,32},{32,31},{31,30},{30,29},{37,-1},{36,35},{35,34},{34,33},{60,56},{61,57},{62,58},{63,59},{64,60},{65,61},{66,62},{67,63},{68,64},{69,65},{2,2},{6,6},{99,20},{98,19},{91,13},{90,12},{93,15},{92,14},{95,17},{94,16},{97,18},{96,9},{11,11},{10,10},{13,13},{12,12},{15,15},{14,14},{17,17},{16,16},{19,18},{18,21},{116,-1},{48,45},{49,46},{46,43},{47,44},{44,41},{45,42},{42,39},{43,40},{40,37},{41,38},{1,1},{5,5},{9,9},{77,-1},{76,-1},{75,71},{74,70},{73,69},{72,68},{71,67},{70,66},{79,1},{78,0}};

std::map<int, int> map_SiCell_pad_HD_full_wafer = { {344,168},{0,76},{346,146},{347,170},{340,169},{341,190},{342,214},{343,191},{348,127},{349,-1},{298,219},{299,218},{296,242},{297,217},{294,266},{295,265},{292,267},{293,241},{290,288},{291,268},{199,374},{198,392},{195,373},{194,-1},{197,355},{196,356},{191,435},{190,423},{193,-1},{192,436},{270,223},{271,-1},{272,-1},{273,334},{274,333},{275,291},{276,335},{277,315},{278,293},{279,313},{449,431},{448,381},{443,365},{442,384},{441,366},{440,346},{447,382},{446,401},{445,383},{444,364},{108,137},{109,138},{102,182},{103,181},{100,180},{101,204},{106,119},{107,139},{104,160},{105,161},{39,95},{38,-1},{33,58},{32,75},{31,43},{30,44},{37,-1},{36,57},{35,42},{34,74},{438,347},{439,327},{436,325},{437,305},{434,304},{435,326},{432,258},{433,282},{430,306},{431,345},{339,192},{338,238},{335,239},{334,263},{337,216},{336,215},{331,287},{330,262},{333,264},{332,240},{345,147},{6,47},{99,203},{98,159},{91,157},{90,199},{93,200},{92,178},{95,201},{94,179},{97,202},{96,158},{238,317},{239,336},{234,295},{235,296},{236,294},{237,316},{230,426},{231,440},{232,-1},{233,-1},{1,60},{146,82},{147,66},{144,12},{145,51},{142,38},{143,39},{140,23},{141,24},{148,52},{149,53},{133,21},{132,35},{131,20},{130,8},{137,11},{136,36},{135,37},{134,9},{139,10},{138,22},{24,27},{25,13},{26,28},{27,26},{20,2},{21,1},{22,15},{23,14},{28,73},{29,59},{407,162},{406,184},{405,140},{404,163},{403,207},{402,121},{401,164},{400,185},{409,183},{408,208},{379,145},{378,56},{371,41},{370,54},{373,40},{372,25},{375,55},{374,70},{377,71},{376,87},{393,257},{392,281},{88,156},{89,155},{397,234},{396,186},{395,209},{394,233},{82,116},{83,97},{80,99},{81,98},{86,115},{87,177},{84,134},{85,135},{7,45},{245,339},{244,319},{247,297},{246,340},{241,318},{240,338},{243,341},{242,337},{249,321},{248,320},{458,324},{459,344},{450,417},{451,400},{452,416},{453,430},{454,399},{455,415},{456,444},{457,363},{179,419},{178,403},{177,418},{176,432},{175,402},{174,388},{173,385},{172,367},{171,368},{170,387},{253,277},{182,404},{183,434},{180,420},{181,433},{186,405},{187,421},{184,437},{185,406},{188,407},{189,422},{11,32},{10,31},{13,16},{12,6},{15,17},{14,29},{17,4},{16,5},{19,3},{18,30},{62,173},{322,285},{323,307},{320,236},{321,328},{326,261},{327,308},{324,348},{325,286},{328,329},{329,309},{201,375},{200,393},{203,357},{202,394},{205,358},{204,377},{207,359},{206,376},{209,360},{208,395},{77,-1},{76,-1},{75,128},{74,129},{73,91},{72,93},{71,92},{70,110},{79,136},{78,117},{2,78},{8,61},{68,130},{120,79},{121,80},{122,81},{123,49},{124,65},{125,64},{126,19},{127,33},{128,34},{129,7},{414,253},{415,230},{416,254},{417,278},{410,231},{411,205},{412,206},{413,229},{418,323},{419,301},{319,259},{318,284},{313,213},{312,189},{311,-1},{310,-1},{317,237},{316,260},{315,212},{314,235},{3,77},{368,69},{369,88},{366,85},{367,86},{364,105},{365,103},{362,123},{363,122},{360,104},{361,142},{380,106},{381,125},{382,107},{383,126},{384,90},{385,108},{386,89},{387,72},{388,-1},{389,-1},{60,195},{61,193},{258,227},{259,251},{64,150},{65,149},{66,148},{67,109},{252,298},{69,111},{250,299},{251,300},{256,276},{257,228},{254,275},{255,252},{465,361},{464,362},{467,-1},{466,-1},{461,398},{460,380},{463,379},{462,343},{168,349},{169,386},{164,371},{165,350},{166,369},{167,351},{160,353},{161,370},{162,352},{163,389},{9,18},{357,143},{356,144},{355,166},{354,167},{353,211},{352,187},{351,188},{350,-1},{359,165},{358,124},{216,414},{217,443},{214,429},{215,442},{212,397},{213,412},{210,378},{211,396},{218,413},{219,428},{289,289},{288,290},{4,46},{281,314},{280,292},{283,332},{282,331},{285,330},{284,312},{287,311},{286,310},{263,225},{262,248},{261,226},{260,250},{267,247},{266,272},{265,249},{264,274},{269,224},{268,273},{59,171},{58,194},{55,174},{54,197},{57,151},{56,196},{51,176},{50,153},{53,198},{52,152},{63,172},{115,-1},{114,102},{117,63},{116,-1},{111,101},{110,100},{113,120},{112,118},{119,50},{118,48},{429,283},{428,-1},{421,279},{420,255},{423,303},{422,302},{425,322},{424,280},{427,-1},{426,342},{308,245},{309,222},{300,243},{301,269},{302,271},{303,270},{304,244},{305,220},{306,246},{307,221},{229,438},{228,408},{227,424},{226,425},{225,410},{224,409},{223,439},{222,441},{221,427},{220,411},{391,232},{390,256},{151,68},{150,83},{153,84},{152,67},{155,-1},{154,-1},{157,390},{156,391},{159,372},{158,354},{399,141},{398,210},{48,175},{49,154},{46,131},{47,133},{44,112},{45,132},{42,94},{43,113},{40,114},{41,96},{5,62} };

std::map<int, int> map_HGCROC_pin_HD_full_wafer = { {344,31},{0,0},{346,33},{347,34},{340,27},{341,28},{342,29},{343,30},{348,35},{349,-1},{298,60},{299,61},{296,58},{297,59},{294,56},{295,57},{292,54},{293,55},{290,53},{199,40},{198,39},{195,36},{194,-1},{197,38},{196,37},{191,34},{190,33},{193,-1},{192,35},{270,35},{271,-1},{272,-1},{273,36},{274,37},{275,38},{276,39},{277,40},{278,41},{279,42},{449,55},{448,54},{443,50},{442,49},{441,48},{440,47},{446,53},{445,52},{444,51},{108,29},{109,30},{102,23},{103,24},{100,21},{101,22},{106,27},{107,28},{104,25},{105,26},{39,36},{38,-1},{33,32},{32,31},{31,30},{30,29},{37,-1},{36,35},{35,34},{34,33},{438,45},{439,46},{436,43},{437,44},{434,41},{435,42},{432,39},{433,40},{430,37},{431,38},{339,26},{338,25},{335,22},{334,21},{337,24},{336,23},{331,18},{333,20},{332,19},{345,32},{6,6},{99,20},{98,19},{91,13},{90,12},{93,15},{92,14},{95,17},{94,16},{97,18},{238,4},{239,5},{234,0},{235,1},{236,2},{237,3},{230,70},{231,71},{232,-1},{233,-1},{1,1},{146,64},{147,65},{144,62},{145,63},{142,60},{143,61},{140,58},{141,59},{148,66},{149,67},{133,52},{132,51},{131,50},{130,49},{137,55},{136,54},{134,53},{139,57},{138,56},{24,23},{25,24},{26,25},{27,26},{20,19},{21,20},{22,21},{23,22},{28,27},{29,28},{407,17},{406,16},{405,15},{404,14},{403,13},{402,12},{401,11},{400,10},{409,18},{379,63},{378,62},{371,55},{370,54},{373,57},{372,56},{375,59},{374,58},{377,61},{376,60},{393,3},{392,2},{88,10},{89,11},{397,7},{396,6},{395,5},{394,4},{82,4},{83,5},{80,2},{81,3},{86,8},{87,9},{84,6},{85,7},{7,7},{245,11},{244,10},{247,13},{246,12},{241,7},{240,6},{243,9},{242,8},{249,15},{248,14},{458,64},{459,65},{450,56},{451,57},{452,58},{453,59},{454,60},{455,61},{456,62},{457,63},{179,22},{178,21},{177,20},{176,19},{175,18},{173,17},{172,16},{171,15},{170,14},{253,18},{182,25},{183,26},{180,23},{181,24},{186,29},{187,30},{184,27},{185,28},{188,31},{189,32},{11,11},{10,10},{13,13},{12,12},{15,15},{14,14},{17,17},{16,16},{19,18},{62,58},{322,10},{323,11},{320,8},{321,9},{326,14},{327,15},{324,12},{325,13},{328,16},{329,17},{201,42},{200,41},{203,44},{202,43},{205,46},{204,45},{207,48},{206,47},{209,50},{208,49},{77,-1},{76,-1},{75,71},{74,70},{73,69},{72,68},{71,67},{70,66},{79,1},{78,0},{2,2},{8,8},{68,64},{120,39},{121,40},{122,41},{123,42},{124,43},{125,44},{126,45},{127,46},{128,47},{129,48},{414,23},{415,24},{416,25},{417,26},{410,19},{411,20},{412,21},{413,22},{418,27},{419,28},{319,7},{318,6},{313,1},{312,0},{311,-1},{310,-1},{317,5},{316,4},{315,3},{314,2},{3,3},{368,53},{366,51},{367,52},{364,49},{365,50},{362,47},{363,48},{360,45},{361,46},{380,64},{381,65},{382,66},{383,67},{384,68},{385,69},{386,70},{387,71},{388,-1},{389,-1},{60,56},{61,57},{258,23},{259,24},{64,60},{65,61},{66,62},{67,63},{69,65},{250,16},{251,17},{256,21},{257,22},{254,19},{255,20},{465,71},{464,70},{467,-1},{466,-1},{461,67},{460,66},{463,69},{462,68},{168,12},{169,13},{164,8},{165,9},{166,10},{167,11},{160,4},{161,5},{162,6},{163,7},{9,9},{357,42},{356,41},{355,40},{354,39},{353,38},{352,37},{351,36},{350,-1},{359,44},{358,43},{216,56},{217,57},{214,54},{215,55},{212,53},{210,51},{211,52},{218,58},{219,59},{289,52},{288,51},{4,4},{281,44},{280,43},{283,46},{282,45},{285,48},{284,47},{287,50},{286,49},{263,28},{262,27},{261,26},{260,25},{267,32},{266,31},{265,30},{264,29},{269,34},{268,33},{59,55},{58,54},{55,52},{54,51},{56,53},{51,48},{50,47},{53,50},{52,49},{63,59},{115,-1},{114,35},{117,36},{116,-1},{111,32},{110,31},{113,34},{112,33},{119,38},{118,37},{429,36},{428,-1},{421,30},{420,29},{423,32},{422,31},{425,34},{424,33},{427,-1},{426,35},{308,70},{309,71},{300,62},{301,63},{302,64},{303,65},{304,66},{305,67},{306,68},{307,69},{229,69},{228,68},{227,67},{226,66},{225,65},{224,64},{223,63},{222,62},{221,61},{220,60},{391,1},{390,0},{151,69},{150,68},{153,71},{152,70},{155,-1},{154,-1},{157,1},{156,0},{159,3},{158,2},{399,9},{398,8},{48,45},{49,46},{46,43},{47,44},{44,41},{45,42},{42,39},{43,40},{40,37},{41,38},{5,5},{18,14}, {57,60}, {96,13}, {135,54}, {174,14}, {213,60}, {252,13}, {291,54}, {330,14}, {369,60}, {408,13}, {447,54} };

#endif // __map_channel_numbers_h__
