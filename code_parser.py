class MoveCommand(object):
	def __init__(self):
		self.resource = ''
		self.point = []
		self.offset_point = []
		self.speed = []
		self.time = []
		self.interpolation = 0
		self.wait_interpolation = True
		self.velocity = []
		self.velocity_time = []

class CodeParser(object):

	def __init__(self):
		self.name = ''
		self.args = []

		self.command_name = ''
		self.command_parameters = ''
	def WriteFile(self, file_name = "foo.txt"):
		# Open a file
		fo = open(file_name, "wb")
		fo.write( "Define SortEncoderBaseFromBin <arg1> <arg2>\n");
		fo.write( "Move larm to [point_a, point_b] shifted [offset_a, offset_b] at [1.0, 2.0]\n");
		# Close opend file
		fo.close()

	def ParseLine(self, line):
		line = line.strip("\n")
		
		parsed_line = line.split(' ')	


		if parsed_line[0] == 'Define':
			self.name = parsed_line[1]
			for i in xrange(2, len(parsed_line)):
				arg = parsed_line[i].strip('<').strip('>')
				self.args.append(arg)

		if parsed_line[0] == 'Move':

			self.command_name = parsed_line[0]
			move = MoveCommand()
			move.resource = parsed_line[1]

			index_start = parsed_line.index('to') + 1
			index_end = parsed_line.index('shifted')

			tmp = ''
			for x in xrange(index_start, index_end):
				tmp = tmp + parsed_line[x]

			move.point = tmp.strip('[').strip(']').split(',')

			index_start = parsed_line.index('shifted') + 1
			index_end = parsed_line.index('at')

			tmp = ''
			for x in xrange(index_start, index_end):
				tmp = tmp + parsed_line[x]

			move.offset_point = tmp.strip('[').strip(']').split(',')

			return move


	def ReadFile(self, file_name="foo.txt"):
		# Open a file
		with open(file_name, "r") as f:
			data = f.readlines()

			lines = []
			for line in data:
				lines.append(line)

		return lines

if __name__=='__main__':
	cp = CodeParser()
	cp.WriteFile()
	cp.ReadFile()
