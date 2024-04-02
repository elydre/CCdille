package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type tokenType struct {
	tType string
	intValue int
	stringValue string
}

func str_split(s string) []string {
	var result []string
	var temp string

	s = strings.Replace(s, "\t", " ", -1)
	s = strings.Replace(s, "\n", " ", -1)
	s = strings.Replace(s, "\r", " ", -1)

	for _, c := range s {
		if c == ' ' {
			if temp != "" {
				result = append(result, temp)
				temp = ""
			}
		} else if c == '(' || c == ')' || c == ';' {
			if temp != "" {
				result = append(result, temp)
				temp = ""
			}
			result = append(result, string(c))
		} else {
			temp += string(c)
		}
	}
	
	if temp != "" {
		result = append(result, temp)
	}

	return result
}


func tokenize(s string) []tokenType {
	var result []tokenType
	stringList := str_split(s)

	for _, str := range stringList {
		val, err := strconv.Atoi(str)

		if err == nil {
			result = append(result, tokenType{"int", val, ""})
		} else if strings.ContainsAny(str, "+-*/") {
			result = append(result, tokenType{"operator", 0, str})
		} else if strings.ContainsAny(str, "()") {
			result = append(result, tokenType{"paren", 0, str})
		} else if str == ";" {
			result = append(result, tokenType{"scolon", 0, str})
		} else {
			result = append(result, tokenType{"string", 0, str})
		}
	}

	return result
}

func printToken(t tokenType) {
	fmt.Print(t.tType, "\t")
	if t.tType == "int" {
		fmt.Print(t.intValue)
	} else {
		fmt.Print(t.stringValue)
	}
	fmt.Println()
}

func read_file(file string) string {
	f, err := os.Open(file)
	if err != nil {
		fmt.Println(err)
		return ""
	}

	fi, err := f.Stat()
	if err != nil {
		fmt.Println(err)
		return ""
	}

	size := fi.Size()
	data := make([]byte, size)
	_, err = f.Read(data)
	if err != nil {
		fmt.Println(err)
		return ""
	}

	return string(data)
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: ", os.Args[0], " <filename>")
		return
	}

	file := os.Args[1]
	data := read_file(file)

	tokens := tokenize(data)

	for _, t := range tokens {
		printToken(t)
	}
}
