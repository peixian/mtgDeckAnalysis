#!/Users/peixianwang/.rvm/bin/rvm-auto-ruby
require 'csv'
mainboard = CSV.read('mainboard.csv')
sideboard = CSV.read('sideboard.csv')

#puts the data out (THIS IS A TEST)
mainboard.each do |row|
  row[0] = row[0].to_f
end 

mainboard.sort_by! {|row| row[1]}


deckNumber = 32
#mainboardUnique = mainboard.uniq{|row| row[1]}
mainboardUnique = mainboard.clone
mainboardUnique.uniq! {|row| row[1]}

mainboard.each do |row|
  puts row.inspect
end

mainboardUnique.sort_by! {|row| row[1]}

mainboardUnique.each do |mbuRow|
  mainboard.each do |mbRow|
    if mbRow[1] == mbuRow[1]
   #   puts mbRow.inspect
      mbuRow[0] += mbRow[0]
    end
  end
end

puts "\n\n\n\n"

mainboardUnique.each do |row|
  row[0] /= deckNumber
  temp = row[1]
  row[1] = row[0]
  row[0] = temp
  puts row.inspect
end