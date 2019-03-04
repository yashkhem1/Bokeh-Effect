import torch
import torch.nn as nn



###### Pix2Pix Utilities ##########################################################

class downConv(nn.Module):
	def __init__(self, in_layer, out_layer, take_norm=True):
		super(downConv, self).__init__()
		self.conv = nn.Conv2d(in_layer, out_layer, kernel_size=4, stride=2, padding=1)
		self.act = nn.LeakyReLU(0.2, True)
		self.norm = nn.BatchNorm2d(out_layer)
		self.take_norm = take_norm

	def forward(self, x):
		x = self.conv(x)
		if self.take_norm:
			return self.act(self.norm(x))
		else :
			return self.act(x)

class upConv(nn.Module):
	def __init__(self, in_layer, out_layer):
		super(upConv, self).__init__()
		self.convt = nn.ConvTranspose2d(in_layer, out_layer, kernel_size=4, stride=2, padding=1)
		self.act = nn.ReLU(True)
		self.norm = nn.BatchNorm2d(out_layer)

	def forward(self, x):
		x = self.act(self.norm(self.convt(x)))
		return x

class Generator(nn.Module):
	def __init__(self, n_downsample=2):
		super(Generator, self).__init__()
		model = [downConv(3, 64, take_norm=False)]
		model += [downConv(64, 128)]
		model += [downConv(128, 256)]
		model += [downConv(256, 512)]
		for i in range(n_downsample):
			model += [downConv(512, 512)]

		for i in range(n_downsample):
			model += [upConv(512, 512)]

		model += [upConv(512, 256)]
		model += [upConv(256, 128)]
		model += [upConv(128, 64)]
		model += [nn.ConvTranspose2d(64, 3, kernel_size=4, stride=2, padding=1)]
		model += [nn.ReLU(True)]
		model += [nn.Tanh()]

		self.model = nn.Sequential(*model)

	def forward(self, x):
		return self.model(x)

# if __name__ == '__main__':
# 	data = torch.randn(1, 3, 256, 256)
# 	model = Generator()
# 	# model2 = downConv(3, 64)
# 	# print(model)
# 	print(model(data).size())	

#######################################################################################