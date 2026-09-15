package main

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/xuri/excelize/v2"
)

func main() {
	// Проверяем аргументы командной строки
	if len(os.Args) < 3 {
		fmt.Println("Использование: excel_service <input.json> <output.xlsx>")
		os.Exit(1)
	}

	jsonPath := os.Args[1]
	outputExcel := os.Args[2]

	// 1. Читаем JSON файл
	file, err := os.ReadFile(jsonPath)
	if err != nil {
		fmt.Printf("Ошибка чтения файла: %v\n", err)
		os.Exit(1)
	}

	var data []map[string]interface{}
	if err := json.Unmarshal(file, &data); err != nil {
		fmt.Printf("Ошибка парсинга JSON: %v\n", err)
		os.Exit(1)
	}

	if len(data) == 0 {
		fmt.Println("Набор данных пуст.")
		os.Exit(1)
	}

	// 2. Создаем Excel документ
	f := excelize.NewFile()
	defer f.Close()

	sheet := "Сводка по студиям"
	f.SetSheetName("Sheet1", sheet)

	// 3. Вытаскиваем заголовки
	// var headers []string
	// for k := range data[0] {
	// 	headers = append(headers, k)
	// }
	headers := []string{
		"Компания",
		"Страна",
		"Количество игр",
		"Средний рейтинг",
		"Лучшая игра",
	}
	// Создаем стиль (Синяя заливка, белый жирный текст, по центру)
	style, err := f.NewStyle(&excelize.Style{
		Font:      &excelize.Font{Bold: true, Color: "FFFFFF"},
		Fill:      excelize.Fill{Type: "pattern", Color: []string{"4F81BD"}, Pattern: 1},
		Alignment: &excelize.Alignment{Horizontal: "center", Vertical: "center"},
	})

	// 4. Записываем заголовки и применяем стиль
	for i, header := range headers {
		cell, _ := excelize.CoordinatesToCellName(i+1, 1)
		f.SetCellValue(sheet, cell, header)
		f.SetCellStyle(sheet, cell, cell, style)

		// Получаем букву колонки (A, B, C...) и ставим ширину 25
		colName, _ := excelize.ColumnNumberToName(i + 1)
		f.SetColWidth(sheet, colName, colName, 25)
	}

	// 5. Записываем данные
	for rowIdx, rowData := range data {
		for colIdx, header := range headers {
			cell, _ := excelize.CoordinatesToCellName(colIdx+1, rowIdx+2)
			// Если значение nil (null в JSON), записываем пустую строку
			val := rowData[header]
			if val == nil {
				val = ""
			}
			f.SetCellValue(sheet, cell, val)
		}
	}

	// 6. Сохраняем файл
	if err := f.SaveAs(outputExcel); err != nil {
		fmt.Printf("Ошибка сохранения Excel: %v\n", err)
		os.Exit(1)
	}

	fmt.Printf("[GO SERVICE] Успешно сгенерирован файл: %s\n", outputExcel)
}
